# AWS Config Rules and Remediation

In this lab, we'll be implementing and enforcing an AWS Config rule related to RDS instances.

### Setup AWS Config

3. Navigate to the AWS Config Console and click Get started.
4. Click the button to turn on recording.
5. Under Amazon S3 bucket*, click Create a bucket You should be able to keep the default Bucket name.
6. Under Amazon SNS topic, click Stream configuration changes and notifications to an Amazon SNS topic.
7. Click Create a topic. The default name should be fine.
7. Under AWS Config role*, click Create AWS Config service-linked role.
8. Click Next.
9. On the AWS Config rules screen, filter by RDS and select rds-instance-public-access-check.
10. Click Next.
11. Click Confirm.
10. Navigate to the RDS dashboard and review the MySQL instance that's running. Notice that the Public accessibility attribute is set to No.
11. Navigate to back to AWS Config and click Rules and note that our rule is listed as Compliant.

### Implement a Custom Rule in AWS Config

1. Navigate to the Lambda console, and open the RDS Log Persistence function. Review the code and copy the function ARN.
2. Navigate back to the Config console and click Add Rule followed by Add custom Rule.
3. Name the rule rds\_log\_persistence and paste the Lambda function ARN in the appropriate box.
4. Select Configuration changes for Trigger type.
5. Select RDS:DBInstance for Resources.
5. Leave the rest of the options at their default values and click Save.
6. Within a few minutes, the rule should evaluate and the rule should show 1 noncompliant resource(s) for Compliance status.
7. Navigate to the RDS console, select the database and click Modify.
8. Scroll down to the Log exports section and select the General log.
9. Click Continue and then click Modify DB Instance.
10. Within a few minutes, the rule should show Compliant for Compliance status.

### Implement Auto-Remediation with AWS Lambda

1. Navigate to the Lambda console and open the RDS Remediation function.
2. Review the code and then click Add trigger.
3. Select SNS and select the topic created during AWS Config setup.
4. Click Add.
5. Navigate back to the RDS console, select the database and click Modify.
6. Scroll down to the Log exports section and de-select the General log.
7. Click Continue and then click Modify DB Instance.
8. The rule will revert to noncompliant status briefly but our remediation function will correct the issue in short order.
