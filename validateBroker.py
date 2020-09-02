import json
import boto3
import botocore
from decimal import Decimal
from boto3.dynamodb.conditions import Key, Attr

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('broker_users')

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)
    
def lambda_handler(event, context):
    email = event.get('email', '').lower() # Mandatory
    password = event.get('password', '') # Mandatory
    userType = event.get('userType', '') # Mandatory
    
    if len(email) == 0:
        return {"statusCode": 500,
                "message": "Error: Please provide an Email!"
                }
    elif len(password) == 0:
        return {"statusCode": 500,
                "message": "Error: Please provide an Email!"
                }
    elif userType != 'broker':
        return {"statusCode": 500,
                "message": "Please invoke the correct API!"
                }
    else:
        response = table.get_item(
            Key={
                'email': email
            }
        )
        
        if 'Item' in response:
            
            companyName = response['Item']['companyName']
    
            filter_expression = Attr('companyName').eq(companyName) & Attr('accountType').eq('root')
                     
            response1 = table.scan(
                FilterExpression=filter_expression
            )
        
            del response1['Items'][0]['password']

            dbPassword = response['Item']['password']
            
            if password == dbPassword:
                if "password" in response['Item']:
                    del response['Item']['password']
                response['Item']['company'] = response1['Items'][0]
                return {
                    "isBase64Encoded": "true",
                    "statusCode": 200,
                    "body": json.dumps(response['Item'], default=default),
                }
            else:
                return {
                        "isBase64Encoded": "true",
                        "statusCode": 500,
                        "body": json.dumps({"message": "Invalid Password!"})
                    }
        else:
            return {
                    "isBase64Encoded": "true",
                    "statusCode": 500,
                    "body": json.dumps({"message": "Email Id not registered!"})
                }
