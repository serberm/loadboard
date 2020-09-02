import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('load_board')

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)
    
def sendResponse(response):
    if 'Item' in response and len(response['Item']) > 0:
        return {
                "isBase64Encoded": "true",
                "statusCode": 200,
                "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
                "body": json.dumps(response['Item'], default=default)
            }
    elif 'Items' in response and len(response['Items']) > 0:
        return {
                "isBase64Encoded": "true",
                "statusCode": 200,
                "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
                "body": json.dumps(response['Items'], default=default)
            }
    else:
        return {
                "isBase64Encoded": "true",
                "statusCode": 500,
                "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
                "body": json.dumps({"message": "Error: Please provide a valid Company Name!"})
            }

# GET Single Item Response
def lambda_handler(event, context):
    
    companyName = event['queryStringParameters']['companyName']
    
    response = table.query(
        IndexName='companyName-index',
        KeyConditionExpression=Key('companyName').eq(companyName)
    )
    
    return sendResponse(response)
    