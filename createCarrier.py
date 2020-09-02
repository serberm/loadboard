import boto3
import botocore
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('carrier_users')

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
    nscNumber = event.get('nscNumber', '') # Mandatory
    if nscNumber != '':
        item['nscNumber'] = nscNumber
    dotNumber = event.get('dotNumber', '') # Mandatory
    if dotNumber != '':
        item['dotNumber'] = dotNumber
    mcNumber = event.get('mcNumber', '') # Mandatory
    if mcNumber != '':
        item['mcNumber'] = mcNumber
    carrierName = event.get('carrierName', '') # Mandatory
    item['carrierName'] = carrierName
    phoneNumber = event.get('phoneNumber', '')
    if phoneNumber != '':
        item['phoneNumber'] = phoneNumber
    aboutUs = event.get('aboutUs', '')
    if aboutUs != '':
        item['aboutUs'] = aboutUs
    websiteURL = event.get('websiteURL', '')
    if websiteURL != '':
        item['websiteURL'] = websiteURL
    trailerCapacity = event.get('trailerCapacity', '')
    if trailerCapacity != '':
        item['trailerCapacity'] = trailerCapacity
    equipment = event.get('equipment', '')
    if equipment != '':
        item['equipment'] = equipment
    operatingProvinces = event.get('operatingProvinces', '')
    if operatingProvinces != '':
        item['operatingProvinces'] = operatingProvinces
    operatingState = event.get('operatingState', '')
    if operatingState != '':
        item['operatingState'] = operatingState
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
    elif companyAddress == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Company Address!"
                }
    elif carrierName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Broker Name!"
                }
    elif nscNumber == '' and dotNumber == '' and mcNumber == '':
        return {"statusCode": 500,
                "message": "Error: Please provide either of NSC#, Dot# or MC#!"
                }
    else:
        print(item)
        try:
            # if the email was already registered in an earlier CSV contact upload by some broker, then keep the contact information and update all the rest
            old_account = table.get_item(
                Key = {
                        "email": email
                    }
            )
            if 'Item' in old_account and len(old_account['Item']) > 0:
                item['contacts'] = old_account['Item'].get('contacts', [])
                table.delete_item(
                    Key={
                        'email': event.get('email', '')
                    }
                )
            table.put_item(
                # Item={'email': email, 'password':  password, 'companyName': companyName, 'companyAddress':  companyAddress, 'nscNumber': nscNumber, 'dotNumber': dotNumber, 'mcNumber':  mcNumber, 'carrierName': carrierName, 'phoneNumber':  phoneNumber, 'aboutUs': aboutUs, 'websiteURL': websiteURL, 'trailerCapacity':  trailerCapacity, 'equipment': equipment, 'operatingProvinces': operatingProvinces}
                Item=item 
            )
            return {"statusCode": 200,
                    "email": email,
                    "name": carrierName
                }
        except Exception as e:
            return {"statusCode": 500,
                    "message": e
                }
