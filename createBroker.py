import boto3
import botocore
import json

from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('broker_users')

def lambda_handler(event, context):
    item = {}
    email = event.get('email', '').lower() # Mandatory
    item['email'] = email
    password = event.get('password', '') # Mandatory
    item['password'] = password
    companyName = event.get('companyName', '') # Mandatory
    item['companyName'] = companyName
    companyAddress = event.get('companyAddress', '') # Mandatory
    item['companyAddress'] = companyAddress
    brokerName = event.get('brokerName', '') # Mandatory
    item['brokerName'] = brokerName
    phoneNumber = event.get('phoneNumber', '')
    accountType = event.get('accountType', '') # Mandatory
    item['accountType'] = accountType
    
    if phoneNumber != '':
        item['phoneNumber'] = phoneNumber
    aboutUs = event.get('aboutUs', '')
    if aboutUs != '':
        item['aboutUs'] = aboutUs
    websiteURL = event.get('websiteURL', '')
    if websiteURL != '':
        item['websiteURL'] = websiteURL
    measurement = event.get('measurement', '')
    if measurement != '':
        item['measurement'] = measurement
    subscription = event.get('subscription', {})
    item['subscription'] = subscription
    
    if email == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Email!"
                }
    elif password == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Password!"
                }
    elif companyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Company Name!"
                }
    elif accountType == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an AccountType!"
                }
    elif brokerName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Broker Name!"
                }
    else:
        try:
            table.put_item(
                # Item={'email': email, 'password':  password, 'companyName': companyName, 'companyAddress':  companyAddress, 'brokerName': brokerName, 'phoneNumber': phoneNumber, 'aboutUs':  aboutUs, 'measurement': measurement}
                Item=item
            )
            return {"statusCode": 200,
                    "email": email,
                    "name": brokerName
                }
        except Exception as e:
            return {"statusCode": 500,
                    "message": "Error: Unable to save record!"
                    }
