import boto3
import datetime
import json

def lambda_handler(event, context):
    
    todays_date = datetime.date.today()
    print(todays_date)
    print(todays_date - datetime.timedelta(days=1))
    
    dynamoDB = boto3.client('dynamodb')
    response = dynamoDB.query(
        ExpressionAttributeValues={
            ':v1': {
                'S': str(todays_date - datetime.timedelta(days=1)),
            },
        },
        KeyConditionExpression='expiration_date = :v1',
        IndexName='expiration_date_index',
        TableName='product_expirations',
    )
    
    for obj in response['Items']:
        portfolio_id = obj['portfolio_id']['S']
        print(portfolio_id)
        product_id = obj['product_id']['S']
        print(product_id)
        
        service_catalog = boto3.client('servicecatalog')
        response = service_catalog.disassociate_product_from_portfolio(
            ProductId=product_id,
            PortfolioId=portfolio_id
        )
        print(response)
