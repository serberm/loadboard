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
    email = event.get('email', '') # Mandatory
    companyAddress = event.get('companyAddress', '') # Mandatory
    phoneNumber = event.get('phoneNumber', ' ')
    aboutUs = event.get('aboutUs', ' ')
    websiteURL = event.get('websiteURL', ' ')
    trailerCapacity = event.get('trailerCapacity', ' ')
    equipment = event.get('equipment', ' ')
    operatingProvinces = event.get('operatingProvinces', ' ')
    operatingState = event.get('operatingState', ' ')
    
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
                UpdateExpression='SET #attr1 = :val1, #attr2 = :val2, #attr3 = :val3, #attr4 = :val4, #attr5 = :val5, #attr6 = :val6, #attr7 = :val7, #attr8 = :val8',
                ConditionExpression=(
                        'email = :email'
                ),
                ExpressionAttributeNames={'#attr1': 'companyAddress', '#attr2': 'phoneNumber', '#attr3': 'aboutUs', '#attr4': 'websiteURL', '#attr5': 'trailerCapacity', '#attr6': 'equipment', '#attr7': 'operatingProvinces', '#attr8': 'operatingState'},
                ExpressionAttributeValues={':email': email, ':val1': companyAddress, ':val2': phoneNumber, ':val3': aboutUs, ':val4': websiteURL, ':val5': trailerCapacity, ':val6': equipment, ':val7': operatingProvinces, ':val8': operatingState},
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
