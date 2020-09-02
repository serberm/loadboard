import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('carrier_capacity')

def lambda_handler(event, context):
    capacityId = event.get('id') # Mandatory
    
    print(capacityId)
    
    try:
        response = table.delete_item(
            Key={
                'id': capacityId
            }
        )
        
        return {"statusCode": 200,
                "message": "Carrier Capacity deleted Successfully!"
            }
    except Exception as e:
        return {"statusCode": 500,
                "message": e
            }
