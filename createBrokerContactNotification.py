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
    brokerEmail = event.get('brokerEmail', '') # Mandatory
    item['brokerEmail'] = brokerEmail
    carrierEmail = event.get('carrierEmail', '') # Mandatory
    item['carrierEmail'] = carrierEmail
    carrierEmail = event.get('carrierEmail', '') # Mandatory
    item['carrierEmail'] = carrierEmail
    carrierEmail = event.get('carrierEmail', '') # Mandatory
    item['carrierEmail'] = carrierEmail
    accept = event.get('accept', '') # Mandatory
    item['accept'] = accept
    createdAt = event.get('notificationDate', '') # Mandatory
    item['createdAt'] = createdAt
    
    if brokerCompanyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Broker Company Name!"
                }
    elif carrierCompanyName == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a Carrier Company Name!"
                }
    elif carrierEmail == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Email Id for Carrier!"
                }
    elif brokerEmail == '':
        return {"statusCode": 500,
                "message": "Error: Please provide an Email Id for Broker!"
                }
    elif accept == '':
        return {"statusCode": 500,
                "message": "Error: Please provide a value for whether the contact is approved!"
                }
    else:
        print(item)
        try:
            table.put_item(
                Item=item 
            )
            return {"statusCode": 200,
                    "message": "Carrier Contacts added Successfully!"
                }
        except Exception as e:
            return {"statusCode": 500,
                    "message": e
                }
