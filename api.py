import requests
import json

def callPenton(fieldname, cacheID):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response_data = requests.get('https://vendor2-mock.herokuapp.com/penton/'+fieldname+'/'+cacheID, headers=headers)

    return response_data.json()

def callVerisk(fieldname, cacheID):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    response_data = requests.get('https://vendor1-mock.herokuapp.com/verisk/'+fieldname+'/'+cacheID, headers=headers)

    return response_data.json()

def get(event, context):
    veriskID = event['queryStringParameters']['veriskID']
    pentonID = event['queryStringParameters']['pentonID']
    fieldname = 'numEmployees'

    pentonResponse = callPenton(fieldname, pentonID)
    veriskResponse = callVerisk(fieldname, veriskID)

    chosenValue = {};
    decisionReason = "";
    chosenVendor = "";

    if(pentonResponse['value'] is not None):
        chosenValue = pentonResponse
        decisionReason = 'Penton had a value'
        chosenVendor = 'Penton'
    else:
        chosenValue = veriskResponse
        decisionReason = 'Penton Didn\'t had a value'
        chosenVendor = 'Verisk'

    responseDict = {"value": chosenValue['value'],  "chosenVendor": chosenVendor, "decisionReason": decisionReason}
        
    return {"body": json.dumps(responseDict, ensure_ascii=False), "statusCode": 200}
