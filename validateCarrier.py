import json
import boto3
import botocore
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('carrier_users')

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
    elif userType != 'carrier':
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
            dbPassword = response['Item']['password']
            
            if password == dbPassword:
                if "password" in response['Item']:
                    del response['Item']['password']
                return {
                        "isBase64Encoded": "true",
                        "statusCode": 200,
                        "body": json.dumps(response['Item'], default=default)
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
