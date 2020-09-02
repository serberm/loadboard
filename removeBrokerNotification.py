import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('notify_broker')

def lambda_handler(event, context):
    notificationId = event.get('id') # Mandatory
    
    print(notificationId)
    
    try:
        response = table.delete_item(
            Key={
                'id': notificationId
            }
        )
        
        return {"statusCode": 200,
                "message": "Notification deleted Successfully!"
            }
    except Exception as e:
        return {"statusCode": 500,
                "message": e
            }
