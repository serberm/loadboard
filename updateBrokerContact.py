import json
import boto3
import botocore
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('broker_contacts')

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def lambda_handler(event, context):
    id = event.get('id', '') # Mandatory
    accept = event.get('accept', '') # Mandatory
    
    try:
        if id == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide a Id!"
                    }
        elif accept == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide an accept status!"
                    }
        else:
            response = table.update_item(
                Key={'id': id},
                UpdateExpression='SET #attr1 = :val1',
                ConditionExpression=(
                        'id = :id'
                ),
                ExpressionAttributeNames={'#attr1': 'accept'},
                ExpressionAttributeValues={':id': id,':val1': accept},
                ReturnValues='ALL_NEW'
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
            return {"code": 500, "message": "id Name does not exists!"}
    except:
        print('Except All')
