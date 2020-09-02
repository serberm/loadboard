import json
import boto3
import botocore
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('broker_users')

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def lambda_handler(event, context):
    email = event.get('email', '') # Mandatory
    reset_token = event.get('reset_token', '')
    reset_timestamp = event.get('reset_timestamp', '')
    
    try:
        if email == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide a valid email!"
                    }
        else:
            response = table.update_item(
                Key={'email': email},
                UpdateExpression='SET #attr1 = :val1, #attr2 = :val2',
                ConditionExpression=(
                        'email = :email'
                ),
                ExpressionAttributeNames={'#attr1': 'reset_token', '#attr2': 'reset_timestamp'},
                ExpressionAttributeValues={':email': email, ':val1': reset_token, ':val2': reset_timestamp},
                ReturnValues='UPDATED_NEW'
            )
        
        print('Response: ', response)
        
        return {
                "isBase64Encoded": "true",
                "statusCode": 200,
                "body": json.dumps(response['Attributes'], default=default)
            }
    except botocore.exceptions.ClientError as e:
        print('Except Boto: ', e)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print('Except if: ', e)
            return {"code": 500, "message": "Email Id does not exists!"}
    except:
        print('Except All')
