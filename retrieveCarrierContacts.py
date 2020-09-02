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
    if  len(response['detailed_contacts']) > 0:
        return {
                "isBase64Encoded": "true",
                "statusCode": 200,
                "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
                "body": json.dumps(response, default=default)
            }
    else:
        return {
                "isBase64Encoded": "true",
                "statusCode": 500,
                "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
                "body": json.dumps({"message": "No records available!"})
            }

# GET Single Item Response
def lambda_handler(event, context):
    
    userEmail = event['queryStringParameters']['userEmail']
    carrier = carrier_table.get_item(
        Key={
            "email": userEmail
        }
    )
    contact_email_list =  carrier.get('Item', {}).get('contacts')
    detailed_contacts = []
    for email in contact_email_list:
        detail = broker_table.get_item(
            Key={"email": email}
        )
        if 'Item' in detail and len(detail['Item']) > 0:
            if 'password' in detail["Item"]:
                del detail["Item"]['password']
            if 'passwordHash' in detail["Item"]:
                del detail["Item"]['passwordHash']
            detailed_contacts.append(detail["Item"])
    
    return sendResponse({
        'detailed_contacts': detailed_contacts,
        'userDetails': carrier.get('Item', {})
    })
    
# import json
# import boto3
# from boto3.dynamodb.conditions import Key, Attr
# from decimal import Decimal

# dynamo_client = boto3.resource('dynamodb')
# table = dynamo_client.Table('carrier_contacts')

# def default(obj):
#     if isinstance(obj, Decimal):
#         return str(obj)
#     raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)
    
# def sendResponse(response):
#     if 'Item' in response and len(response['Item']) > 0:
#         return {
#                 "isBase64Encoded": "true",
#                 "statusCode": 200,
#                 "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
#                 "body": json.dumps(response['Item'], default=default)
#             }
#     elif 'Items' in response and len(response['Items']) > 0:
#         return {
#                 "isBase64Encoded": "true",
#                 "statusCode": 200,
#                 "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
#                 "body": json.dumps(response['Items'], default=default)
#             }
#     else:
#         return {
#                 "isBase64Encoded": "true",
#                 "statusCode": 500,
#                 "headers": { "Access-Control-Allow-Methods": "*", "Access-Control-Allow-Headers": "*", "Access-Control-Allow-Origin": "*" },
#                 "body": json.dumps({"message": "No records ava!"})
#             }

# # GET Single Item Response
# def lambda_handler(event, context):
    
#     carrierCompanyName = event['queryStringParameters']['carrierCompanyName']
#     accept = event['queryStringParameters']['accept']
    
#     response = table.query(
#             IndexName='carrierCompanyName-accept-index',
#             KeyConditionExpression=Key('carrierCompanyName').eq(carrierCompanyName) & Key('accept').eq(accept)
#         )
    
#     return sendResponse(response)
    