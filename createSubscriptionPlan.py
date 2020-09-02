import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('plans')

def lambda_handler(event, context):
    item = {}
    planId = str(uuid.uuid4()) # Auto-Generated
    item['planId'] = planId
    planName = event.get('planName', '') # Mandatory
    item['planName'] = planName
    planType = event.get('planType', '') # Mandatory
    item['planType'] = planType
    basicPrice = event.get('basicPrice', 0) # Mandatory
    item['basicPrice'] = basicPrice
    totalPrice = event.get('totalPrice', 0) # Mandatory
    item['totalPrice'] = totalPrice
    
    if planName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Plan Name!"
                }
    elif planType == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Plan Type!"
                }
    elif basicPrice <= 0:
        return {"statusCode": 500,
                "message": "Error: Please provide a valid Basic Price!"
                }
    elif totalPrice <= 0:
        return {"statusCode": 500,
                "message": "Error: Please provide a valid Total Price!"
                }
    else:
        print(item)
        try:
            table.put_item(
                # Item={'email': email, 'password':  password, 'companyName': companyName, 'companyAddress':  companyAddress, 'nscNumber': nscNumber, 'dotNumber': dotNumber, 'mcNumber':  mcNumber, 'carrierName': carrierName, 'phoneNumber':  phoneNumber, 'aboutUs': aboutUs, 'websiteURL': websiteURL, 'trailerCapacity':  trailerCapacity, 'equipment': equipment, 'operatingProvinces': operatingProvinces}
                Item=item 
            )
            return {"statusCode": 200,
                    "message": "Plan added Successfully!"
                }
        except Exception as e:
            return {"statusCode": 500,
                    "message": e
                }
