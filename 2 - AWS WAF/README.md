# Automating WAF IP List Updates with AWS Lambda

## Setup Artillery Instances
   <details>
    <summary> Adjust the default security group settings in the default vpc to allow ssh access from your ip.</summary>
    
    1. Navigate to the EC2 dashboard and click on Security groups under Resources.
    2. Click the check-box next to the security group with a Group Name of "defualt" and open the Inbound tab.
    3. Click the Edit button and on the Edit inbound rules dialog box click the Add Rule button. 
    4. Set Type to "SSH", Source to "My IP" and click the Save button.

   </details>
   <details>
    <summary>Create and download a key pair.</summary>
    
    1. Navigate to the EC2 dashboard and click on Keys pairs under Resources.
    2. Click on Create Key Pair, enter a name, and click Create.
    3. Download the Key.
    
   </details>
   <details>
    <summary>Launch the artillery instances.</summary>
    
    1. Navigate to the EC2 dashboard and click on Running instances under Resources.
    2. Click the Launch Instance button.
    3. In Step 1: Choose an Amazon Machine Image, open the My AMIs tab and select the artillery image.
    4. In Step 2: Choose an Instance Type, take the default and click on Next: Configure Instance Details.
    5. In Step 3: Configure Instance Details, make the following changes:
       Configuration Option | Value
       ---------------------|------
       Number of instances | 2
       Auto-assign Public IP | Disable
       
   </details>

2. Review the Resources Being Protected
3. Complete Setup of WAF
4. Configure Lambda Function
