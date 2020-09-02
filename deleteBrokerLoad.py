import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('load_board')

def lambda_handler(event, context):
    loadId = event.get('id') # Mandatory
    
    print(loadId)
    
    try:
        response = table.delete_item(
            Key={
                'id': loadId
            }
        )
        
        return {"statusCode": 200,
                "message": "Broker Load deleted Successfully!"
            }
    except Exception as e:
        return {"statusCode": 500,
                "message": e
            }
