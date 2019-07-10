import os

import pymongo
import requests
import json
import re
from config import *
from requests import RequestException

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]


def page_index():
    response = requests.get('https://lol.qq.com/biz/hero/champion.js')
    data = response.text
    json1 = re.findall(r"LOLherojs.champion=(.+?);", data)
    hero_json = json.loads(json1[0])['keys']
    #print(type(hero_json))
    all_url = []
    print(hero_json.items())
    for key, value in hero_json.items():
        url = 'https://lol.qq.com/biz/hero/' + str(value) +'.js'
        all_url.append(url)
    return all_url


def parse_page_detail(url):
    response = requests.get(url)
    data = response.text
    value = url.split('/')[-1].split('.')[0]
    deleteinfo = 'LOLherojs.champion.'+str(value)
    json1 = re.findall(r""+str(deleteinfo)+"=(.+?);", data)
    hero_json = json.loads(json1[0])['data']
    hero_json_name = hero_json['name']
    hero_json_skins = hero_json['skins']
    all_infos = []
    all_info = dict()
    for skin in hero_json_skins:
        id = skin['id']
        name = skin['name']
        if name =='default':
            name = '默认皮肤'
        else:
            name = skin['name']
        imageurl = 'http://ossweb-img.qq.com/images/lol/web201310/skin/small'+str(id)+'.jpg'
        all_info = {'hero':hero_json_name,
                    'skin':name,
                    'imageurl':imageurl
                    }
        all_infos.append(all_info)
    return all_infos


def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('存储到mongodb成功',result)
        return True
    return False

def down_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
    except RequestException:
        print("下载图片页出错了", url)
        return None
def save_image(url,hero_name,skin_name):
    try:
        response = requests.get(url)
        if  skin_name.find('/') == -1:
            pass
        else:
            skin_name = skin_name.replace('/', '／')
        print(skin_name)
        if response.status_code == 200:
            content = response.content
            path = 'D:/python/eclipse-workspace/p/' + str(hero_name)
            file_path = '{0}/{1}.{2}'.format(path, skin_name, 'jpg')
            if os.path.exists(path):
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(content)
                        f.close()
            else:
                os.mkdir(path)
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(content)
                        f.close()
        else:
            print("下载图片页出错了", url)
    except RequestException:
        print("下载图片页出错了", url)
        return None


if __name__=="__main__":
    (all_url) = page_index()
    for url in all_url:
        result = parse_page_detail(url)
        for heroinfo in result:
            hero_name = heroinfo['hero']
            skin_name = heroinfo['skin']
            url = heroinfo['imageurl']
            save_image(url,hero_name,skin_name)



