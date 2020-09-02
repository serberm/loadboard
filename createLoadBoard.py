import boto3
import botocore
import json
import uuid
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
table = dynamo_client.Table('load_board')

def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)

def lambda_handler(event, context):
    item = {}
    identifier = str(uuid.uuid4())
    item['id'] = identifier
    email = event.get('email', '') # Mandatory
    item['email'] = email
    companyName = event.get('companyName', '') # Mandatory
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
    isPrivate = event.get('isPrivate', 'No')
    item['isPrivate'] = isPrivate
    dh_o = event.get('dh_o', '')
    if dh_o != '':
        item['dh_o'] = dh_o
    destinationTownOrCity = event.get('destinationTownOrCity', '') # Mandatory
    item['destinationTownOrCity'] = destinationTownOrCity
    destinationProvOrState = event.get('destinationProvOrState', '') # Mandatory
    item['destinationProvOrState'] = destinationProvOrState
    postDate = event.get('postDate', '') # Mandatory
    item['postDate'] = postDate
    dh_d = event.get('dh_d', '')
    if dh_d != '':
        item['dh_d'] = dh_d
    rate = event.get('rate', '')
    if rate != '':
        item['rate'] = rate
    phoneNumber = event.get('phoneNumber', ' ')
    if phoneNumber != '':
        item['phoneNumber'] = phoneNumber
    partialInfo = event.get('partialInfo', '')
    if partialInfo != '':
        item['partialInfo'] = partialInfo
    reeferInfo = event.get('reeferInfo', '')
    if reeferInfo != '':
        item['reeferInfo'] = reeferInfo
    notes = event.get('notes', '')
    if notes != '':
        item['notes'] = notes
    isNew = event.get('isNew')
    boardId = event.get('id')
    coordinators = event.get('coordinators')
    item['coordinators'] = coordinators
    if email == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Email!"
                }
    elif companyName == '':
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
    # elif phoneNumber == '':
    #     return {"statusCode": 500,
    #             "message": "Error: Please provide the Phone Number!"
    #             }
    elif postDate == '':
        return {"statusCode": 500,
                "message": "Error: Please provide the Load Post Date!"
                }
    else:
        try:
            
            if isNew:
                response = table.put_item(
                    # Item={'id': identifier, 'coordinators': coordinators, email':  email, 'companyName':  companyName, 'commodity': commodity, 'equipment':  equipment, 'loadType': loadType, 'pickupDateTime': pickupDateTime, 'origin':  origin, 'dh_o': dh_o, 'destination': destination, 'dh_d': dh_d, 'rate':  rate, 'phoneNumber': phoneNumber, 'partialInfo': partialInfo, 'reeferInfo': reeferInfo, 'notes': notes}
                    Item=item
                )
            else:
                response = table.update_item(
                    Key={'id': boardId},
                    UpdateExpression='SET #attr1 = :val1, #attr2 = :val2, #attr3 = :val3, #attr4 = :val4, #attr5 = :val5, #attr6 = :val6, #attr7 = :val7, #attr8 = :val8, #attr9 = :val9, #attr10 = :val10, #attr11 = :val11, #attr12 = :val12, #attr13 = :val13, #attr14 = :val14, #attr15 = :val15, #attr16 = :val16, #attr17 = :val17, #attr18 = :val18, #attr19 = :val19, #attr20 = :val20',
                    ConditionExpression=(
                        'id = :id'
                    ),
                    ExpressionAttributeNames={'#attr1': 'email', '#attr2': 'companyName', '#attr3': 'commodity', '#attr4': 'equipment', '#attr5': 'loadType', '#attr6': 'pickupDateTime', '#attr7': 'originTownOrCity', '#attr8': 'dh_o', '#attr9': 'destinationTownOrCity', '#attr10': 'dh_d', '#attr11': 'rate', '#attr12': 'phoneNumber', '#attr13': 'partialInfo', '#attr14': 'reeferInfo', '#attr15': 'notes', '#attr16': 'coordinators', '#attr17': 'originProvOrState', '#attr18': 'destinationProvOrState', '#attr19': 'isPrivate', '#attr20': 'postDate'},
                    ExpressionAttributeValues={':id': boardId, ':val1': email, ':val2': companyName, ':val3': commodity, ':val4': equipment, ':val5': loadType, ':val6': pickupDateTime, ':val7': originTownOrCity, ':val8': dh_o, ':val9': destinationTownOrCity, ':val10': dh_d, ':val11': rate, ':val12': phoneNumber, ':val13': partialInfo, ':val14': reeferInfo, ':val15': notes, ':val16': coordinators, ':val17': originProvOrState, ':val18': destinationProvOrState, ':val19': isPrivate, ':val20': postDate},
                    ReturnValues='UPDATED_NEW'
                )
            if isNew:
                return {
                    "statusCode": 200,
                    "message": "Data Added Successfully to Load Board!",
                    "boardId": response["Item"]["id"]
                }
            else:
                return {
                    "statusCode": 200,
                    "message": "Data Edited Successfully to Load Board!",
                    "boardId": boardId
                }
        except Exception as e:
            return {
                "statusCode": 500,
                "message": "Error: Unable to save record!"
                }
