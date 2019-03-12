
import apiai
import json
import sys
sys.path.insert(0, '../helper')
from helper.config import CLIENT_ACCESS_TOKEN

'''ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
request = ai.text_request()
request.lang = 'zh-TW'  

request.query = 'aa'
response = request.getresponse()

try:
    result = json.loads(str(response.read(), encoding = "utf-8")) 

    if 'get_gym_name' in result['result']['parameters']:
        print('yes')
    else:
        print('no')
    print(result)
    print('-----')
    print(result['result']['fulfillment']['speech'])
    print(result['result']['parameters']['get_gym_name'])

except Exception as e:
    print('intent nlp exception: '+ str(e))'''


def get_GYM_NAME(msg):

    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.lang = 'zh-TW'
    request.query = msg
    response = request.getresponse()

    try:
        result = json.loads(str(response.read(), encoding = "utf-8")) 
        print(result)

        if 'get_gym_name' in result['result']['parameters']:
            
            response = dict()
            response["isOk"] = True
            response["response"] = result['result']['fulfillment']['speech']
            response["gymName"] = result['result']['parameters']['get_gym_name']
            return response
        else:
            
            response = dict()
            response["isOk"] = False
            response["response"] = result['result']['fulfillment']['speech']
            response["gymName"] = "None"
            return response

    except Exception as e:
        print('intent nlp exception: '+ str(e))

