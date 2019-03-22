#https://iplay.sa.gov.tw/api/GymSearchAllList?$format=application/json;odata.metadata=none&Keyword=%E5%9C%8B%E6%B0%91%E9%81%8B%E5%8B%95%E4%B8%AD%E5%BF%83&Latitude=25.000265&Longitude=121.461814
#https://iplay.sa.gov.tw//odata/Gym(9627)
#A:中山運動中心 南港運動中心 信義運動中心 大安運動中心 文山運動中心 內湖運動中心 蘆洲國民運動中心 土城國民運動中心 汐止國民運動中心 永和國民運動中心 朝馬國民運動中心 中壢國民運動中心 桃園國民運動中心 竹光國民運動中心
#B:板橋國民運動中心 中正運動中心 （中和國民運動中心 官網無提供即時資訊）

import requests
import json
from bs4 import BeautifulSoup
import re
import time

#14
A_site = {'中山運動中心': 'cssc', '南港運動中心': 'ngsc', '信義運動中心': 'xysc', '大安運動中心': 'dasc', '文山運動中心': 'wssc', 
          '內湖運動中心': 'nhsc', '蘆洲國民運動中心': 'lzcsc', '土城國民運動中心': 'tccsc', '汐止國民運動中心': 'xzcsc', '永和國民運動中心': 'yhcsc',
          '朝馬國民運動中心': 'cmcsc', '中壢國民運動中心': 'zlcsc', '桃園國民運動中心': 'tycsc', '竹光國民運動中心': 'zgcsc'}
#2
B_site = {'板橋國民運動中心': 'bqsports', '中正運動中心': 'tpejjsports'}

#5
C_site = {'北投運動中心': 0, '大同運動中心': 2, '士林運動中心': 6, '松山運動中心': 7, '萬華運動中心': 8}



def current_people(area):

    if area in A_site.keys():
        res = get_A_site(area)
        return res

    elif area in B_site.keys():
        res = get_B_site(area)
        return res
    
    elif area in C_site.keys():
        res = get_C_site(area)
        return res
    
    elif area in Other_site.keys():
        res = Other_site[area]
        return res

    else:
        return False


def get_A_site(area):

    print("開始準備擷取...")
    res = []
    r = requests.get('https://'+ A_site[area] + '.cyc.org.tw/api')

    if r.status_code == requests.codes.ok:
        jsonData = json.loads(r.text)
        
        for i in range(0, 2):
                res.append(jsonData["gym"][:-1][i])
                res.append(jsonData["swim"][:-1][i])
        #print(jsonData["gym"][:-1])
        #print(jsonData["swim"][:-1])
        res[1], res[2] = res[2], res[1]

        print(area+"抓取完成")
        print(res)
        return res
    else:
        print(area+"擷取失敗...")
        return
    

def get_B_site(area):
    
    print("開始準備擷取...")
    res = []
    r = requests.get('http://www.' + B_site[area] + '.com.tw/zh-TW/onsitenum?wmode=opaque')
    
    if r.status_code == requests.codes.ok:
        soup = BeautifulSoup(r.text, "html.parser")
        #print(soup.find_all("span"))
        for i in range(0, 4):
            #print(soup.find_all("span")[i].text[:-1])
            res.append(soup.find_all("span")[i].text[:-1])
        
        print(area+"抓取完成")
        print(res)
        return res
    else:
        print(area+"擷取失敗...")
        return      
    

def get_C_site(area):

    print("開始準備擷取...")
    res = []
    r = requests.post('http://booking.tpsc.sporetrofit.com/Home/loadLocationPeopleNum')
    
    if r.status_code == requests.codes.ok:
        #print(r.text)
        jsonData = json.loads(r.text)
        x = C_site[area]
        #print(jsonData["locationPeopleNums"][x])
        res.append(jsonData["locationPeopleNums"][x]["gymPeopleNum"])
        res.append(jsonData["locationPeopleNums"][x]["gymMaxPeopleNum"])
        res.append(jsonData["locationPeopleNums"][x]["swPeopleNum"])
        res.append(jsonData["locationPeopleNums"][x]["swMaxPeopleNum"])

        print(area+"抓取完成")
        print(res)
        return res
    else:
        print(area+"擷取失敗...")
        return 


# 南平
def get_NP_site():

    print("開始準備擷取...")
    res = []
    r = requests.get('https://www.npsc.com.tw/counter.txt')
    #try https://www.npsc.com.tw/counter.txt
    
    if r.status_code == requests.codes.ok:

        tmp = r.text.split(',')
        res.append(tmp[0])
        res.append('75')
        res.append(tmp[1])
        res.append('150')

        print("南平運動中心抓取完成")
        print(res)
        time.sleep(0.1)
        return res
    else:
        print("南平運動中心擷取失敗...")
        time.sleep(0.1)
        return 


#淡水
def get_TS_site():

    print("開始準備擷取...")
    res = []
    r = requests.get('http://www.tssc.tw/')

    if r.status_code == requests.codes.ok:
   
        soup = BeautifulSoup(r.text, "html.parser")
        #print(soup.prettify())
        #print(soup.find_all("span", class_="number-current"))
        #print(soup.find_all("span", class_="number-max"))
        
        for i in range(0, 2):
            res.append(soup.find_all("span", class_="number-current")[i].text)
            res.append(re.sub('\D', '', soup.find_all("span", class_="number-max")[i].text))
        
        res.reverse()
        res[0], res[1] = res[1], res[0]
        res[2], res[3] = res[3], res[2]

        print("淡水運動中心抓取完成")
        print(res)
        time.sleep(0.1)
        return res
    else:
        print("淡水運動中心擷取失敗...")
        time.sleep(0.1)
        return 


#三鶯
def get_SY_site():

    res = []
    r = requests.get('https://scysports.com.tw/')

    if r.status_code == requests.codes.ok:

        soup = BeautifulSoup(r.text, "html.parser")
        #print(soup.prettify())
        #print(soup.find_all(class_="notice"))
        #print(soup.find_all("span")[:2])
        
        for i in range (0, 2):
            res.append(soup.find_all(class_="notice")[0:2][i].text)
            res.append(re.sub('\D', '', soup.find_all("span")[:2][i].text))

        print("三鶯運動中心抓取完成")
        print(res)
        time.sleep(0.1)
        return res
    else:
        print("三鶯運動中心擷取失敗...")
        time.sleep(0.1)
        return


#鶯歌 健身房資訊only
def get_YG_site():

    res = []
    r = requests.get('https://scysports.com.tw/')

    if r.status_code == requests.codes.ok:
    
        soup = BeautifulSoup(r.text, "html.parser")
        #print(soup.prettify())
        #print(soup.find_all(class_="notice"))
        #print(soup.find_all("span")[:3])
        res.append(soup.find_all(class_="notice")[2:3][0].text)
        res.append(re.sub('\D', '', soup.find_all("span")[2:3][0].text))
        res.append('0')
        res.append('0')

        print("鶯歌運動中心抓取完成")
        print(res)
        time.sleep(0.1)
        return res
    else:
        print("鶯歌運動中心擷取失敗...")
        time.sleep(0.1)
        return

####################
#other
Other_site = {'南平運動中心': get_NP_site(), '淡水國民運動中心': get_TS_site(), '三鶯國民運動中心': get_SY_site(), '鶯歌國民運動中心': get_YG_site()}
