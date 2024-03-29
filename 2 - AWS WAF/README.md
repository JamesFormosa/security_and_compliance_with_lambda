# Automating WAF IP List Updates with AWS Lambda

## Setup Artillery Instances

\* You'll need the name of your ArtilleryFilesBucket from the Resources section of WAF Lab CloudFormation stack. This is the value in the field labeled Physical ID.

### Adjust the default security group settings in the default vpc to allow ssh access from your ip.
    
1. Navigate to the EC2 dashboard and click on Security groups under Resources.
2. Click the check-box next to the security group with a Group Name of "defualt" and open the Inbound tab.
3. Click the Edit button and on the Edit inbound rules dialog box click the Add Rule button. 
4. Set Type to "SSH", Source to the security group of your Cloud9 instance.

### Create and download a key pair.
    
From a Cloud9 terminal window run the following:

```
mkdir waf_lab
cd waf_lab
aws ec2 create-key-pair --key-name buckeye-key --query 'KeyMaterial' --output text > buckeye-key.pem
```

### Launch the artillery instances.
    
1. Navigate to the EC2 dashboard and click on Running instances under Resources.
2. Click the Launch Instance button.
3. In Step 1: Choose an Amazon Machine Image, open the My AMIs tab, click Shared with me and select the artillery image.
4. In Step 2: Choose an Instance Type, take the default and click Next: Configure Instance Details.
5. In Step 3: Configure Instance Details, make the following changes:

Configuration Option | Value
---------------------|------
Number of instances | 2
Auto-assign Public IP | Disable
IAM Role | ArtilleryInstanceProfile

6. Paste the following code into the User data section, inserting the name of your bucket as indicated. 

```bash
#!/bin/bash
sudo yum update -y
cd /home/ec2-user
aws s3 cp s3://YOUR-BUCKET-HERE . --recursive
```

7. Take the defult in Step 4: Add Storage and click Next: Add tags
8. In Step 5: Add Tags, click Next: Configure Security Group
9. In Step 6: Configure Security Group, click the Select an existing security group option and then select the default security group. Click Review and Launch
10. In Step 7: Review Instance Launch, click Launch.
11. In the Key Pair dialog, ensure your key is selected, check the box acknowledging your access to the key file and click Launch Instance.

\* It should take no more than 2-3 minutes for the instances to launch and pass status checks.

12. Once the instances are created, navigate to Elastic IPs in the Resources section of the EC2 dashboard.
13. Select the first elastic IP and click Actions->Associate Elastic IP address
14. On the Associate Elastic IP address screen, leave Instance selected and then choose one of your EC2 instances.
15. Click Associate.
16. Repeat 12-15 for the second Elastic IP and instance.

## WAF Setup

### Review the Resources Being Protected

In this lab, our WAF is protecting a simple API that provides GET / PUT access to a DynamoDB table through AWS service integration.

1. Navigate to the API Gateway console and select the API.
2. Inspect the RESTful interface and then navigate to Stages.
3. Click on the tst stage and copy and save the Invoke Url for use a little later.
4. Navigate to the DynamoDB console and briefly inspect te table. This is a very simple table with a composite key based on market and date.

### Complete Setup of WAF

1. Navigate to the WAF & Shield console.
2. Click on Go to AWS WAF.
3. Click on IP Sets and select the appropriate region. Notice that an IP set containing one of our elastic IPs has already been created.
4. Click on Web ACLs and then click Create web ACL
5. Give the Web ACL a name and then click Add AWS resources.
6. Leave API Gateway selected and select the tst stage. Click Add and then click Next.
7. Click Add rules->Add my own rules and rule groups.
8. We're going to create a rule to allow are business partners and block everyone else. Leave Rule Builder selected and give the rule a name.
9. From the Inspect drop-down, select Originates from an IP address in and select our IP Set.
10. Change Action to Allow and click Add.
11. Change Default action to Block and click Next.
12. Click Next on the Set rule priority screen.
13. Click Next on the Configure metrics screen.
14. Click Create web ACL

### Test the Web ACL

Based on our current setup, one of our EC2 instances should have access to the API; the other should not. Let's test it.

1. Connect to the instance that has an IP in our IP Set. The commands for doing this can be copied from the EC2 console by seleting the insatce and clicking Connect. For the ssh command, change root@ to ec2-user@.
2. Once logged run ls at the prompt and confirm that test.yaml and trades.csv are present.
3. Set the TARGET variable by running the following command and replacing the target with the Invoke Url copied earlier.
```
export TARGET="YOUR-TST-STAGE-ENDPOINT-HERE"
```
4. Run the following command to test access. You should receive response codes of 200.
```
artillery run test.yaml
```
5. Repeat steps 1-4 for the second instance. You shgould receive reposnse codes of 403. 
\* If for some reason you get response codes of 200, confirm that the tst stage is associated withn the Web ACL and the defaule action is set to Block. These are easy steps to miss.

## Automation with Lambda

### Configure Lambda Function

Going to the console to update our IP Lists is always an option but not one that will scale as our business partnerships grow. A more viable approach will involve some sort of automation, a goal for which AWS Lambda is very well-suited. In this section, we'll explore this option by implementing a very simple lambda function for updating our IP Lists.

1. Navigate to the Lambda console and open the UpdateIPListFunction. The code was provided through ClodFormation, but there are a few configuration changes we need to make here.
2. Our WAF implementation relies on WAFv2 which was released less than a month ago and is only available in the newest version of the Python Boto3 library. This version is not yet available in the Boto3 libraries that are included in the AWS Lambda runtimes. We'll leverage Lambda layers to overcome this limitation.
3. Navigate to Layers in the Lambda console and click Create Layer.
4. Name the layer boto3\_1\_10\_28 and upload the python.zip file located in the folder of that name under 4 - Resources.
5. Once the layer is complete, navigate back to Functions console and re-open the UpdateIPListFunction.
6. Click on Layers, scroll to the bottom of the function and click Add a layer.
7. Select the layer just created and click Add.
8. Click configure test events and add a new test event based on the HelloWorld template.
9. Name the new test event and paste the follwoing json in to the payload.
```
{
  "ip_set_name": "IP-SET-NAME-HERE",
  "ip_set_id": "IP-SET-ID-HERE",
  "scope": "REGIONAL",
  "new_ip":"SECOND-IP-ADDRESS-HERE/32"
}
```
10. Click Save.
11. Click Test from the function console.
12. Navigate to the IP Set and confirm that there are now two approved IP addresses in our IP Set.
13. Log back into the second EC2 instance and re-run the following command. You shgould receive response codes of 200 this time.
```
artillery run test.yaml
```