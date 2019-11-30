import boto3
import json

def get_db_identifier(resource_id):
    rds = boto3.client('rds')
    response = rds.describe_db_instances(
        Filters=[
            {
                'Name': 'dbi-resource-id',
                'Values': [
                    resource_id
                ]
            }    
        ]
    )
    return response['DBInstances'][0]['DBInstanceIdentifier']

def enable_cloudwatch_export(db_identifier):
    rds = boto3.client('rds')
    response = rds.modify_db_instance(
        DBInstanceIdentifier=db_identifier,
        CloudwatchLogsExportConfiguration={
            'EnableLogTypes':['general']
        }
    )
    print(response)

def lambda_handler(event, context):
    print(event['Records'][0]['Sns']['Message'])
    config_notification = json.loads(event['Records'][0]['Sns']['Message'])
    if ('resourceType' in config_notification) and ('newEvaluationResult' in config_notification):
        print('Process this one...')
        if (config_notification['resourceType'] == 'AWS::RDS::DBInstance') and (config_notification['configRuleName'] == 'rds_log_persistence'):
                if(config_notification['newEvaluationResult']['complianceType'] == 'NON_COMPLIANT'):
                    print('OH NO!!! WAKE UP 5,000 PEOPLE!!!')
                    db_identifier = get_db_identifier(config_notification['resourceId'])
                    enable_cloudwatch_export(db_identifier)
                else:
                    print('All good...')