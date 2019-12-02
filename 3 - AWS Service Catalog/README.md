### Setup a Portfolio

1. Navigate to AWS Service Catalog and click on Portfolios and then click Create portfolio.
2. Give your portfolio a name and enter your initials for Owner.
3. Click Create.
4. Click on Products and click Upload new product.
5. Enter Standard Artillery Instance for Product name and enter a brief Description.
6. Enter your initials for Provided by and click Next.
7. Click Next on the Support details screen.
8. On the Version details screen, click Specify a URL location for an Amazon CloudFormation template.
9. Paste the object URL from the standard_artillery.template in your S3 bucket.
10. Enter Standard Artillery Instance and click Next.
11. On the Review screen, click Create.
12. Repeat steps 1-11 for the second template in the S3 bucket, using a name/description of Enhanced Artillery Instance.
13. Click on Portfolios and then click on the portfolio created in step 1.
14. Click Add product to Portfolio and then select the Standard Artillery Instance.
15. Repeat 13-14 for the Enhanced Artillery Instance.

### Create an expiration record

1. Make note of the Portfolio Id and the Product Id for the Enhanced artillery Instance.
2. Navigate to DynamoDB and open then product_expirations table.
3. Click on Items tab and click Create item.
4. Enter Portfolio ID and Product Id in the appropriate fields and enter yesterdays date for the expiration_date.

### Test the Lambda function and expire a product

1. Navigate to the Lambda console and open the Expire Product function.
2. Enter a blank test event in Configure test events.
3. Click Test.
4. Navigate back to the Portfolio we crated and confirm that the Enhanced Artillery Instance has been removed.