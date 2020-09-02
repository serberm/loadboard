import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
broker_table = dynamo_client.Table('broker_users')
carrier_table = dynamo_client.Table('carrier_users')

response = carrier_table.scan()
carrier_emails = []
for i in response['Items']:
    carrier_emails.append(i['email'])

def lambda_handler(event, context):
    userEmail = event["userEmail"]
    broker = broker_table.get_item(
        Key={
            "email": userEmail
        }
    )
    contact_email_list = broker.get('Item', {}).get('contacts', [])
    new_contact_list = []
    new_user_list = []
    for contact in event.get('contacts', []):
        if contact['Email'] not in carrier_emails:
            newCarrier = {}
            newCarrier['email'] = contact['Email']
            newCarrier['companyName'] = contact.get('Company Name', '')
            newCarrier['carrierName'] = contact.get('First Name', '') + ' ' + contact.get('Last Name', '')
            newCarrier['contacts'] = [userEmail]
            newCarrier['temp'] = True
            carrier_table.put_item(
                Item=newCarrier
            )
            new_contact_list.append(contact)
            new_user_list.append(contact)
        
        if contact['Email'] not in contact_email_list:
            contact_email_list.append(contact['Email'])
    try:        
        broker_table.update_item(
            Key={'email': userEmail},
            UpdateExpression='SET #attr1 = :val1',
            ConditionExpression=(
                'email = :email'
            ),
            ExpressionAttributeNames={'#attr1': 'contacts'},
            ExpressionAttributeValues={':email': userEmail, ':val1': contact_email_list},
            ReturnValues='UPDATED_NEW'
        )
        return {
            'statusCode': 200,
            'newContacts': new_user_list
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "message": e
        }
