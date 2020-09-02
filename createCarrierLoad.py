import boto3
import botocore
import uuid
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('carrier_loads')

def lambda_handler(event, context):
    item = {}
    identifier = str(uuid.uuid4())
    item['id'] = identifier
    brokerCompanyName = event.get('brokerCompanyName', '') # Mandatory, this is broker company name
    item['brokerCompanyName'] = brokerCompanyName
    companyName = event.get('companyName', '') # Mandatory, this is carrier company name
    item['companyName'] = companyName
    commodity = event.get('commodity', '')
    if commodity != '':
        item['commodity'] = commodity
    equipment = event.get('equipment', '') # Mandatory
    item['equipment'] = equipment
    loadType = event.get('loadType', '') # Mandatory
    item['loadType'] = loadType
    pickupDateTime = event.get('pickupDateTime', '') # Mandatory
    item['pickupDateTime'] = pickupDateTime
    originTownOrCity = event.get('originTownOrCity', '') # Mandatory
    item['originTownOrCity'] = originTownOrCity
    originProvOrState = event.get('originProvOrState', '') # Mandatory
    item['originProvOrState'] = originProvOrState
    dh_o = event.get('dh_o', '')
    if dh_o != '':
        item['dh_o'] = dh_o
    destinationTownOrCity = event.get('destinationTownOrCity', '') # Mandatory
    item['destinationTownOrCity'] = destinationTownOrCity
    destinationProvOrState = event.get('destinationProvOrState', '') # Mandatory
    item['destinationProvOrState'] = destinationProvOrState
    dh_d = event.get('dh_d', '')
    if dh_d != '':
        item['dh_d'] = dh_d
    partialInfo = event.get('partialInfo', '')
    if partialInfo != '':
        item['partialInfo'] = partialInfo
    reeferInfo = event.get('reeferInfo', '')
    if reeferInfo != '':
        item['reeferInfo'] = reeferInfo
    postDate = event.get('postDate', '') # Mandatory
    item['postDate'] = postDate
    isPrivate = event.get('isPrivate', 'No')
    item['isPrivate'] = isPrivate
    phoneNumber = event.get('phoneNumber', '')
    if phoneNumber != '':
        item['phoneNumber'] = phoneNumber
    notes = event.get('notes', '')
    if notes != '':
        item['notes'] = notes
    rate = event.get('rate', '')
    if rate != '':
        item['rate'] = rate
    
    if companyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Company Name!"
                }
    elif equipment == '':
        return {"statusCode": 500,
                "message": "Error: Please provide the equipment details!"
                }
    elif loadType == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Load Type!"
                }
    elif pickupDateTime == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Pickup Date/Time!"
                }
    elif originTownOrCity == '' or originProvOrState == '':
        return {"statusCode": 500,
                "message": "Error: Please provide the Origin Town/City and Province/State details!"
                }
    elif destinationTownOrCity == '' or destinationProvOrState == '':
        return {"statusCode": 500,
                "message": "Error: Please provide the Destination Town/City and Province/State details!"
                }
    elif postDate == '':
        return {"statusCode": 500,
                "message": "Error: Please provide the  Post Date!"
                }
    else:
        try:
            table.put_item(
                # Item={'id': identifier, 'email':  email, 'companyName':  companyName, 'commodity': commodity, 'equipment':  equipment, 'loadType': loadType, 'pickupDateTime': pickupDateTime, 'origin':  origin, 'dh_o': dh_o, 'destination': destination, 'dh_d': dh_d, 'rate':  rate, 'phoneNumber': phoneNumber, 'partialInfo': partialInfo, 'reeferInfo': reeferInfo, 'notes':  notes}
                Item=item
            )
            return {
                "statusCode": 200,
                "message": "Data Added Successfully to Load Board!"
                }
        except Exception as e:
            return {
                "statusCode": 500,
                "message": "Error: Unable to save record!"
                }
