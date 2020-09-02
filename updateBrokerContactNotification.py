import json
import boto3
import botocore
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('broker_contacts')
broker_table = dynamo_client.Table('broker_users')
carrier_table = dynamo_client.Table('carrier_users')

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
            item = table.get_item(
                Key={
                    "id": id
                }
            )
            if ('Item' in item and len(item['Item']) > 0 and accept == 'yes'):
                brokerEmail = item['Item']['brokerEmail']
                carrierEmail = item['Item']['carrierEmail']
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
                if ('Item' in broker and len(broker['Item']) > 0 and 'Item' in carrier and len(carrier['Item']) > 0):
                    brokerContacts = broker['Item'].get('contacts', [])
                    carrierContacts = carrier['Item'].get('contacts', [])
                    if carrierEmail not in brokerContacts:
                        brokerContacts.append(carrierEmail)
                    if brokerEmail not in carrierContacts:
                        carrierContacts.append(brokerEmail)
                    broker_table.update_item(
                        Key={'email': brokerEmail},
                        UpdateExpression='SET #attr1 = :val1',
                        ConditionExpression=(
                                'email = :email'
                        ),
                        ExpressionAttributeNames={'#attr1': 'contacts'},
                        ExpressionAttributeValues={':email': brokerEmail, ':val1': brokerContacts},
                        ReturnValues='UPDATED_NEW'
                    )
                    carrier_table.update_item(
                        Key={'email': carrierEmail},
                        UpdateExpression='SET #attr1 = :val1',
                        ConditionExpression=(
                                'email = :email'
                        ),
                        ExpressionAttributeNames={'#attr1': 'contacts'},
                        ExpressionAttributeValues={':email': carrierEmail, ':val1': carrierContacts},
                        ReturnValues='UPDATED_NEW'
                    )
                    table.delete_item(
                        Key={
                            'id': id
                        }
                    )
                    return {
                        "isBase64Encoded": "true",
                        "statusCode": 200,
                        "body": json.dumps(brokerContacts)
                    }
            table.delete_item(
                Key={
                    'id': id
                }
            )
            return {
                "statusCode": 500,
                "message": "Internal error!"
            }
        return {
            "statusCode": 500,
            "message": "Internal error!"
        }
    except botocore.exceptions.ClientError as e:
        print('Except Boto: ', e)
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print('Except if: ', e)
            return {"code": 500, "message": "id Name does not exists!"}
    except:
        print('Except All')
