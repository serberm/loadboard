import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
broker_table = dynamo_client.Table('broker_users')
carrier_table = dynamo_client.Table('carrier_users')

def lambda_handler(event, context):
    try:
        carrierEmail = event.get('carrierEmail', '')
        brokerEmail = event.get('brokerEmail', '')
        broker = broker_table.get_item(
            Key={
                "email": brokerEmail
            }
        )
        carrier = carrier_table.get_item(
            Key={
                "email": carrierEmail
            }
        )
        broker_contact_list = broker['Item'].get('contacts', [])
        carrier_contact_list = carrier['Item'].get('contacts', [])
        if (carrierEmail in broker_contact_list):
            broker_contact_list.remove(carrierEmail)
        if (brokerEmail in carrier_contact_list):
            carrier_contact_list.remove(brokerEmail)
        carrier_table.update_item(
            Key={'email': carrierEmail},
            UpdateExpression='SET #attr1 = :val1',
            ConditionExpression=(
                    'email = :email'
            ),
            ExpressionAttributeNames={'#attr1': 'contacts'},
            ExpressionAttributeValues={':email': carrierEmail, ':val1': carrier_contact_list},
            ReturnValues='UPDATED_NEW'
        )
        broker_table.update_item(
            Key={'email': brokerEmail},
            UpdateExpression='SET #attr1 = :val1',
            ConditionExpression=(
                    'email = :email'
            ),
            ExpressionAttributeNames={'#attr1': 'contacts'},
            ExpressionAttributeValues={':email': brokerEmail, ':val1': broker_contact_list},
            ReturnValues='UPDATED_NEW'
        )
        return {"statusCode": 200,
            "message": "Carrier contact deleted Successfully!",
            "body": {
                "contacts": carrier_contact_list,
            }
        }
    except Exception as e:
        return {"statusCode": 500,
                "message": e
            }
