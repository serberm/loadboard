import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('carrier_contacts')

def lambda_handler(event, context):
    item = {}
    notificationId = str(uuid.uuid4()) # Auto-Generated
    item['id'] = notificationId
    brokerCompanyName = event.get('brokerCompanyName', '') # Mandatory
    item['brokerCompanyName'] = brokerCompanyName
    carrierCompanyName = event.get('carrierCompanyName', '') # Mandatory
    item['carrierCompanyName'] = carrierCompanyName
    email = event.get('email', '') # Mandatory
    item['email'] = email
    phoneNumber = event.get('phoneNumber', '') 
    if phoneNumber != '':
        item['phoneNumber'] = phoneNumber
    accept = event.get('accept', '') # Mandatory
    item['accept'] = accept
    hqLocation = event.get('hqLocation', '') # Mandatory
    item['hqLocation'] = hqLocation
    aboutUs = event.get('aboutUs', '')
    if aboutUs != '':
        item['aboutUs'] = aboutUs
    
    if brokerCompanyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Broker Company Name!"
                }
    elif carrierCompanyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Carrier Company Name!"
                }
    elif email == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Email Id for Carrier!"
                }
    # elif phoneNumber == '':
    #     return {"statusCode": 500,
    #             "message": "Error: Please provide a Phone Number for Carrier!"
    #             }
    elif hqLocation == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Carrier HQ Location!"
                }
    elif accept == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a value for whether the contact is approved!"
                }
    else:
        print(item)
        try:
            table.put_item(
                # Item={'email': email, 'password':  password, 'companyName': companyName, 'companyAddress':  companyAddress, 'nscNumber': nscNumber, 'dotNumber': dotNumber, 'mcNumber':  mcNumber, 'carrierName': carrierName, 'phoneNumber':  phoneNumber, 'aboutUs': aboutUs, 'websiteURL': websiteURL, 'trailerCapacity':  trailerCapacity, 'equipment': equipment, 'operatingProvinces': operatingProvinces}
                Item=item 
            )
            return {"statusCode": 200,
                    "message": "Carrier Contacts added Successfully!"
                }
        except Exception as e:
            return {"statusCode": 500,
                    "message": e
                }
