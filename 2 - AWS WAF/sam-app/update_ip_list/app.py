import boto3
import json
import os

def lambda_handler(event, context):
    print(boto3.__version__)
    dirs = os.listdir('/opt')
    for x in dirs:
        print(x)
    waf = boto3.client('wafv2')
    
    response = waf.get_ip_set(
        Name=event['ip_set_name'],
        Scope=event['scope'],
        Id=event['ip_set_id']
    )
    print(response)
    lock_token=response['LockToken']
    addresses=response['IPSet']['Addresses']
    addresses.append(event['new_ip'])
    response = waf.update_ip_set(
        Name=event['ip_set_name'],
        Scope=event['scope'],
        Id=event['ip_set_id'],
        LockToken = lock_token,
        Addresses = addresses
    )
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
