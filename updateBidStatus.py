import json
import boto3
import botocore
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('bids')

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def lambda_handler(event, context):
    bid_id = event.get('bid_id', '') # Mandatory
    status = event.get('status', 'PENDING')
    
    try:
        if bid_id == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide a valid Bid Id!"
                    }
        else:
            response = table.update_item(
                Key={'bid_id': bid_id},
                UpdateExpression='SET #attr1 = :val1',
                ConditionExpression=(
                        'bid_id = :bid_id'
                ),
                ExpressionAttributeNames={'#attr1': 'status'},
                ExpressionAttributeValues={':bid_id': bid_id,':val1': status},
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
            return {"code": 500, "message": "Bid Id does not exists!"}
    except:
        print('Except All')
