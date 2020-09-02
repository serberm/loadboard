import boto3
import botocore
import uuid
from decimal import Decimal

dynamo_client = boto3.resource('dynamodb')
lb_table = dynamo_client.Table('load_board')
b_table = dynamo_client.Table('bids')

def lambda_handler(event, context):
    bid_id = str(uuid.uuid4()) # Auto-Generated
    loadBoardId = event.get('loadBoardId', '') # Mandatory
    companyName = event.get('companyName', '') # Mandatory
    phoneNumber = event.get('phoneNumber', ' ') # Mandatory
    
    email = event.get('email', '') # Mandatory
    offer = event.get('offer', 0.0) # Mandatory
    offer = Decimal(str(offer))
    status = event.get('status', 'PENDING')
    
    # Retrieving the Load Board Details from Load Board table for Validation
    response = lb_table.get_item(
            Key={
                'id': loadBoardId
            }
        ) 
    
    # If the load borad id is valid, then proceed further
    if 'Item' in response and len(response['Item']) > 0:
        if companyName == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide the Carrier Company Name!"
                    }
        elif email == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide the Carrier Email!"
                    }
        # elif phoneNumber == '':
        #     return {"statusCode": 500,
        #             "message": "Error: Please provide the Carrier Phone Number!"
        #             }
        elif offer == '':
            return {"statusCode": 500,
                    "message": "Error: Please provide the Carrier Offer!"
                    }
        else:
            try:
                b_table.put_item(
                    Item={'bid_id': bid_id, 'loadBoardId': loadBoardId, 'email':  email, 'companyName':  companyName, 'phoneNumber': phoneNumber, 'offer': offer, 'status': status}
                )
                return {
                    "statusCode": 200,
                    "message": "Added a bid successfully!"
                    }
            except Exception as e:
                return {
                    "statusCode": 500,
                    "message": "Error: Unable to save record!"
                    }
    else:
        return {
                "isBase64Encoded": "true",
                "statusCode": 500,
                "body": json.dumps({"message": "Error: Please provide a valid Load Board ID!"})
            }
    