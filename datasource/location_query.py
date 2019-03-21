import requests
import json


def gym_search(lon, lat):

    r = requests.get('https://iplay.sa.gov.tw/api/GymSearchAllList?$format=application/json;odata.metadata=none&Keyword=國民運動中心&LandAttr=公有(不含學校、公園、運動園區)&Latitude='+lat+'&Longitude='+lon)

    if r.status_code == requests.codes.ok:
        #print(r.text)
        jsonData = json.loads(r.text)
        #print(len(jsonData))
        #print(jsonData)
        jsonData = sorted(jsonData, key=lambda x: x['Distance'])
        #print(jsonData[:3])
        
        #non empty
        if jsonData:
            response = dict()
            response["isOk"] = True
            response["response"] = jsonData[:3]
            return response
        else:
            response = dict()
            response["isOk"] = False
            response["response"] = "None"
            return response

    else:
        print('search gym api fail')
        return 


def gym_detail(id):

    r = requests.get('https://iplay.sa.gov.tw//odata/Gym('+ str(id) +')?$format=application/json;odata.metadata=none')
    if r.status_code == requests.codes.ok:
        #print(r.text)
        result = json.loads(r.text, encoding = "utf-8")
        response = dict()
        response["web"] = result["WebUrl"]
        return response
    else:
        print(id + 'search detail api fail')
        return


def gym_address(name):

    gym_name = name

    r = requests.get('https://iplay.sa.gov.tw/api/GymSearchAllList?$format=application/json;odata.metadata=none&Keyword='+ gym_name +'&LandAttr=公有(不含學校、公園、運動園區)')

    if r.status_code == requests.codes.ok:
        #print(r.text)
        jsonData = json.loads(r.text)
        #print(jsonData[0]["Address"])

        return jsonData[0]["Address"]
    else:
        print(name + 'cannot get address')