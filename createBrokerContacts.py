import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('broker_contacts')

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
    originProvOrState = event.get('originProvOrState', '') # Mandatory
    item['originProvOrState'] = originProvOrState
    destinationProvOrState = event.get('destinationProvOrState', '') # Mandatory
    item['destinationProvOrState'] = destinationProvOrState
    equipmentTypes = event.get('equipmentTypes', '') # Mandatory
    item['equipmentTypes'] = equipmentTypes
    hqLocation = event.get('hqLocation', '') # Mandatory
    item['hqLocation'] = hqLocation
    aboutUs = event.get('aboutUs', '')
    if aboutUs != '':
        item['aboutUs'] = aboutUs
    accept = event.get('accept', '') # Mandatory
    item['accept'] = accept
    # Either of NSC#, DOT# or MC# is mandatory
    nscNumber = event.get('nscNumber', '') # Mandatory
    if nscNumber != '':
        item['nscNumber'] = nscNumber
    dotNumber = event.get('dotNumber', '') # Mandatory
    if dotNumber != '':
        item['dotNumber'] = dotNumber
    mcNumber = event.get('mcNumber', '') # Mandatory
    if mcNumber != '':
        item['mcNumber'] = mcNumber
    
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
    elif originProvOrState == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Origin Province or State!"
                }
    elif destinationProvOrState == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Destination Province or State!"
                }
    elif equipmentTypes == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Carrier Equipment Types!"
                }
    elif hqLocation == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Broker HQ Location!"
                }
    # elif aboutUs == '':
    #     return {"statusCode": 500,
    #             "message": "Error: Please provide a Carrier About US description!"
    #             }
    elif nscNumber == '' and dotNumber == '' and mcNumber == '':
        return {"statusCode": 500,
                "message": "Error: Please provide either of NSC#, Dot# or MC#!"
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
                    "message": "Broker Contacts added Successfully!"
                }
        except Exception as e:
            return {"statusCode": 500,
                    "message": e
                }
