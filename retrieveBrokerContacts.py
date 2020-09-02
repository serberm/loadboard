import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('broker_contacts')
broker_table = dynamo_client.Table('broker_users')
carrier_table = dynamo_client.Table('carrier_users')

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)
    
def sendResponse(response):
    return {
            "isBase64Encoded": "true",
            "statusCode": 200,
            "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
            "body": json.dumps(response, default=default)
        }


# GET Single Item Response
def lambda_handler(event, context):
    
    userEmail = event['queryStringParameters']['userEmail']
    user = broker_table.get_item(
        Key={
            "email": userEmail
        }
    )
    companyName =  user.get('Item', {}).get('companyName')
    
    filter_expression = Attr('companyName').eq(companyName)

    brokers = broker_table.scan(
        FilterExpression=filter_expression
    )
    detailed_contacts = []
    for broker in brokers['Items']:
        contact_email_list =  broker.get('contacts', []);
        for email in contact_email_list:
            detail = carrier_table.get_item(
                Key={"email": email}
            )
            if 'Item' in detail and len(detail['Item']) > 0:
                if 'password' in detail["Item"]:
                    del detail["Item"]['password']
                if 'passwordHash' in detail["Item"]:
                    del detail["Item"]['passwordHash']
                detail["Item"]['brokerEmail'] = broker['email']
                detailed_contacts.append(detail["Item"])
    
    return sendResponse({
        'detailed_contacts': detailed_contacts,
        'userDetails': user.get('Item', {})
    })
