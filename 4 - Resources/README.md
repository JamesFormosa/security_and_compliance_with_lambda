## Resources

Setup Instructions

Launch a Cloud9 instance with all defaults. As of December 2019, Cloud9 is available in the following regions:

 US | AP | EU
----|----|----
N. Virginia | Singapore | Dublin 
Ohio | Tokyo | Ireland 
Oregon | |

From the Cloud9 bash shell type the following:

```
mkdir git_hub
cd git_hub
git clone https://github.com/JamesFormosa/security_and_compliance_with_lambda
```

If you're doing this on your own, you'll need to build an artillery image. Begin by launching an EC2 instance using the Amazon Linux 2 AMI. Select t2.micro for size and then do the following:

1. Connect to the instance over SSH.
2. Install Node.
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
. ~/.nvm/nvm.sh
nvm install node
```
3. Install Artillery.
```
npm install -g artillery
```
4. Confirm Artillery installation.
```
artillery -V
```
5. Create the image by navigating to the EC2 Dashboard, selecting your image and clicking Actions -> Image -> CreateImage.

Share the product template files

Create an S3 bucket for SAM package files and then run each of the following, inserting the name of your bucket where indicated.

1 - AWS Config Rules and Remediation
```
cd security_and_compliance_with_lambda/1\ -\ AWS\ Config\ Rules\ and\ Remediation/sam-app/
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket [YOUR BUCKET NAME HERE] --s3-prefix config
aws cloudformation deploy --template-file /home/ec2-user/environment/git_hub/security_and_compliance_with_lambda/1\ -\ AWS\ Config\ Rules\ and\ Remediation/sam-app/packaged.yaml --stack-name config-lab-stack  --capabilities CAPABILITY_IAM
```
2 - AWS WAF
```
cd git_hub/security_and_compliance_with_lambda/2\ -\ AWS\ WAF/sam-app/
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket [YOUR BUCKET NAME HERE] --s3-prefix waf
aws cloudformation deploy --template-file /home/ec2-user/environment/git_hub/security_and_compliance_with_lambda/2\ -\ AWS\ WAF/sam-app/packaged.yaml --stack-name waf-lab-stack  --capabilities CAPABILITY_IAM
```
The Lambda functions in the WAF lab require a lambda layer in order to leverage the latest version of Boto3 which includes WAFv2. Do the folowing to setup that layer:

1. Navigate to the Lambda console and click Layers and then click Create layer.
2. Name the layer boto3\_1\_10\_28 and upload the python.zip file located in the boto3\_1\_10\_28 subdirectory in the Resources section of this repo.
3. Select Python 3.7 and Python 3.8 for runtimes and click Create.

An EC2 startup script that thi lab utilizes will download artillery runfiles from an S3 bucket cretated by the script. Do the following to upload those files to that bucket.
1. Navigate to the resources section of the CloudFormation stack and click through to that bucket.
2. Upload the files located in the artillery\_run\_files subdirectory in the Resources section of this repo. 

3 - AWS Service Catalog
```
cd git_hub/security_and_compliance_with_lambda/3\ -\ AWS\ Service\ Catalog/sam-app/
sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket [YOUR BUCKET NAME HERE] --s3-prefix cat
aws cloudformation deploy --template-file /home/ec2-user/environment/git_hub/security_and_compliance_with_lambda/3\ -\ AWS\ Service\ Catalog\/sam-app/packaged.yaml --stack-name cat-lab-stack  --capabilities CAPABILITY_IAM
```
References:

https://github.com/awslabs/aws-config-rules

https://aws.amazon.com/blogs/mt/how-to-update-aws-service-catalog-provisioned-products-to-new-product-versions-and-report-changes-using-aws-step-functions-aws-lambda-and-amazon-athena/