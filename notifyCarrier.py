import boto3
import json
import uuid

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('notify_carrier')

def lambda_handler(event, context):
    item = {}
    notificationId = str(uuid.uuid4()) # Auto-Generated
    item['id'] = notificationId
    brokerCompanyName = event.get('brokerCompanyName', '') # Mandatory
    item['brokerCompanyName'] = brokerCompanyName
    carrierCompanyName = event.get('carrierCompanyName', '') # Mandatory
    item['carrierCompanyName'] = carrierCompanyName
    loadDate = event.get('loadDate', '') # Mandatory
    item['loadDate'] = loadDate
    originTownOrCity = event.get('originTownOrCity', '') # Mandatory
    item['originTownOrCity'] = originTownOrCity
    originProvOrState = event.get('originProvOrState', '') # Mandatory
    item['originProvOrState'] = originProvOrState
    destinationTownOrCity = event.get('destinationTownOrCity', '') # Mandatory
    item['destinationTownOrCity'] = destinationTownOrCity
    destinationProvOrState = event.get('destinationProvOrState', '') # Mandatory
    item['destinationProvOrState'] = destinationProvOrState
    loadId = event.get('loadId', '') # Mandatory
    item['loadId'] = loadId
    
    if brokerCompanyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Broker Company Name!"
                }
    elif carrierCompanyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Carrier Company Name!"
                }
    elif loadDate == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Load Date!"
                }
    elif originTownOrCity == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Origin Town or City!"
                }
    elif originProvOrState == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Origin Province or State!"
                }
    elif destinationTownOrCity == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Destination Town or City!"
                }
    elif destinationProvOrState == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Destination Province or State!"
                }
    elif loadId == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Load Id!"
                }
    else:
        print(item)
        try:
            table.put_item(
                # Item={'email': email, 'password':  password, 'companyName': companyName, 'companyAddress':  companyAddress, 'nscNumber': nscNumber, 'dotNumber': dotNumber, 'mcNumber':  mcNumber, 'carrierName': carrierName, 'phoneNumber':  phoneNumber, 'aboutUs': aboutUs, 'websiteURL': websiteURL, 'trailerCapacity':  trailerCapacity, 'equipment': equipment, 'operatingProvinces': operatingProvinces}
                Item=item 
            )
            return {"statusCode": 200,
                    "message": "Carrier Notification added Successfully!"
                }
        except Exception as e:
            return {"statusCode": 500,
                    "message": e
                }
