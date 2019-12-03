## Resources

Setup Instructions

Launch a Cloud9 instance with all defaults. As of December 2019, Cloud9 is available in the following regions:

 AP | EU | US
----|----|----
Singapore | Dublin | N. Virginia
Tokyo | Ireland | Ohio
 | | Oregon

From the Cloud9 bash shell type the following:

mkdir git_hub
cd git_hub
git clone https://github.com/JamesFormosa/security_and_compliance_with_lambda

Share the artillery image
Share the product template files

1 - AWS Config Rules and Remediation

sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket las-event-### --s3-prefix config

aws cloudformation deploy --template-file /home/ec2-user/environment/git_hub/security_and_compliance_with_lambda/1\ -\ AWS\ Config\ Rules\ and\ Remediation/sam-app/packaged.yaml --stack-name config-lab-stack  --capabilities CAPABILITY_IAM

2 - AWS WAF

cd into git_hub/security_and_compliance_with_lambda/2\ -\ AWS\ WAF/sam-app/

sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket las-event-### --s3-prefix waf

aws cloudformation deploy --template-file /home/ec2-user/environment/git_hub/security_and_compliance_with_lambda/2\ -\ AWS\ WAF/sam-app/packaged.yaml --stack-name waf-lab-stack  --capabilities CAPABILITY_IAM

3 - AWS Service Catalog

cd into git_hub/security_and_compliance_with_lambda/3\ -\ AWS\ Service\ Catalog/sam-app/

sam package --template-file template.yaml --output-template-file packaged.yaml --s3-bucket las-event-### --s3-prefix cat

aws cloudformation deploy --template-file /home/ec2-user/environment/git_hub/security_and_compliance_with_lambda/3\ -\ AWS\ Service\ Catalog\/sam-app/packaged.yaml --stack-name cat-lab-stack  --capabilities CAPABILITY_IAM

References:

https://github.com/awslabs/aws-config-rules

https://aws.amazon.com/blogs/mt/how-to-update-aws-service-catalog-provisioned-products-to-new-product-versions-and-report-changes-using-aws-step-functions-aws-lambda-and-amazon-athena/