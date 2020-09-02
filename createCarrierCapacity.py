import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('carrier_capacity')

def lambda_handler(event, context):
    item = {}
    notificationId = str(uuid.uuid4()) # Auto-Generated
    item['id'] = notificationId
    carrierCompanyName = event.get('carrierCompanyName', '') # Mandatory
    item['carrierCompanyName'] = carrierCompanyName
    carrierEmail = event.get('carrierEmail', '') # Mandatory
    item['carrierEmail'] = carrierEmail
    openDate = event.get('openDate', '') # Mandatory
    item['openDate'] = openDate
    closeDate = event.get('closeDate', '') # Mandatory
    item['closeDate'] = closeDate
    equipment = event.get('equipment', '') # Mandatory
    item['equipment'] = equipment
    loadType = event.get('loadType', '') # Mandatory
    item['loadType'] = loadType
    orignTownOrCity = event.get('orignTownOrCity', '') # Mandatory
    item['orignTownOrCity'] = orignTownOrCity
    originProvOrState = event.get('originProvOrState', '') # Mandatory
    item['originProvOrState'] = originProvOrState
    destTownOrCity = event.get('destTownOrCity', '') # Mandatory
    item['destTownOrCity'] = destTownOrCity
    destProvOrState = event.get('destProvOrState', '') # Mandatory
    item['destProvOrState'] = destProvOrState
    dhOrigin = event.get('dhOrigin', '')
    if dhOrigin != '':
        item['dhOrigin'] = dhOrigin
    dhDest = event.get('dhDest', '')
    if dhDest != '':
        item['dhDest'] = dhDest
    
    if carrierEmail == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Email Id for Carrier!"
                }
    elif carrierCompanyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Carrier Company Name!"
                }
    elif openDate == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a load Open date and time!"
                }
    elif closeDate == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a load Close date and time!"
                }
    elif equipment == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Carrier Equipment!"
                }
    elif loadType == '':
        return {"statusCode": 500,
                "message": "Error: Please provide the Carrier Load Type!"
                }
    elif orignTownOrCity == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Origin Town or City!"
                }
    elif originProvOrState == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Origin Province or State!"
                }
    elif destTownOrCity == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Destination Town or City!"
                }
    elif destProvOrState == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Destination Province or State!"
                }
    # elif dhOrigin == '':
    #     return {"statusCode": 500,
    #             "message": "Error: Please provide a DeadHead Origin!"
    #             }
    # elif dhDest == '':
    #     return {"statusCode": 500,
    #             "message": "Error: Please provide a DeadHead Destination!"
    #             }
    else:
        print(item)
        try:
            table.put_item(
                # Item={'email': email, 'password':  password, 'companyName': companyName, 'companyAddress':  companyAddress, 'nscNumber': nscNumber, 'dotNumber': dotNumber, 'mcNumber':  mcNumber, 'carrierName': carrierName, 'phoneNumber':  phoneNumber, 'aboutUs': aboutUs, 'websiteURL': websiteURL, 'trailerCapacity':  trailerCapacity, 'equipment': equipment, 'operatingProvinces': operatingProvinces}
                Item=item 
            )
            return {"statusCode": 200,
                    "message": "Carrier Capacity added Successfully!"
                }
        except Exception as e:
            return {"statusCode": 500,
                    "message": e
                }
