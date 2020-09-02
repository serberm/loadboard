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
    companyAddress = event.get('companyAddress', '')
    phoneNumber = event.get('phoneNumber', ' ')
    aboutUs = event.get('aboutUs', ' ')
    websiteURL = event.get('websiteURL', ' ')
    
    try:
        if email == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide an Email!"
                    }
        elif companyAddress == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide the Company Address!"
                    }
        else:
            response = table.update_item(
                Key={'email': email},
                UpdateExpression='SET #attr1 = :val1, #attr2 = :val2, #attr3 = :val3, #attr4 = :val4',
                ConditionExpression=(
                        'email = :email'
                ),
                ExpressionAttributeNames={'#attr1': 'companyAddress', '#attr2': 'phoneNumber', '#attr3': 'aboutUs', '#attr4': 'websiteURL'},
                ExpressionAttributeValues={':email': email, ':val1': companyAddress, ':val2': phoneNumber, ':val3': aboutUs, ':val4': websiteURL},
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
