import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('load_board')
broker_table = dynamo_client.Table('broker_users')

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def lambda_handler(event, context):
    response = table.scan()
    data = response['Items']
    
    k = 0
    for load_board in response['Items']:
        companyName =  load_board.get('companyName')
    
        filter_expression = Attr('companyName').eq(companyName)
        
        brokers = broker_table.scan(
            FilterExpression=filter_expression
        )
        detailed_contacts = []
        for broker in brokers['Items']:
            contact_email_list =  broker.get('contacts', [])
            detailed_contacts = detailed_contacts + contact_email_list
        data[k]['contacts'] = detailed_contacts
        k = k + 1
            
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            
            tmpLoadbards = response['Items']
            k = 0
            for load_board in response['Items']:
                companyName =  load_board.get('companyName')
    
                filter_expression = Attr('companyName').eq(companyName)

                brokers = broker_table.scan(
                    FilterExpression=filter_expression
                )
                detailed_contacts = []
                for broker in brokers['Items']:
                    contact_email_list =  broker.get('contacts', [])
                    detailed_contacts = detailed_contacts + contact_email_list
                tmpLoadbards[k]['contacts'] = detailed_contacts
                k = k + 1
            tmpLoadbards[0]['test'] = 3
            data.extend(tmpLoadbards)
        else:
            break
    
    return {
                "isBase64Encoded": "true",
                "statusCode": 200,
                "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
                "body": json.dumps(data, default=default)
            }