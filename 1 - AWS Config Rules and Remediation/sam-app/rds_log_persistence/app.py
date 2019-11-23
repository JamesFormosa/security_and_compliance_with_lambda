import boto3
import json

def is_applicable(config_item, event):
    status = config_item['configurationItemStatus']
    event_left_scope = event['eventLeftScope']
    test = ((status in ['OK', 'ResourceDiscovered']) and
            event_left_scope == False)
    return test
    
def evaluate_compliance(config_item, rule_parameters):
    if (config_item['resourceType'] != 'AWS::RDS::DBInstance'):
        return 'NOT_APPLICABLE'

    elif ('general' in config_item['configuration']['enabledCloudwatchLogsExports']):
        return 'COMPLIANT'
    else:
        return 'NON_COMPLIANT'

def lambda_handler(event, context):
    invoking_event = json.loads(event['invokingEvent'])
    rule_parameters = json.loads(event['ruleParameters'])
    print(invoking_event)
    print(rule_parameters)
    print(invoking_event['configurationItem'])
    
    compliance_value = 'NOT_APPLICABLE'
    
    if is_applicable(invoking_event['configurationItem'], event):
        compliance_value = evaluate_compliance(
                invoking_event['configurationItem'], rule_parameters)

    config = boto3.client('config')
    response = config.put_evaluations(
       Evaluations=[
           {
               'ComplianceResourceType': invoking_event['configurationItem']['resourceType'],
               'ComplianceResourceId': invoking_event['configurationItem']['resourceId'],
               'ComplianceType': compliance_value,
               'OrderingTimestamp': invoking_event['configurationItem']['configurationItemCaptureTime']
           },
       ],
       ResultToken=event['resultToken'])
