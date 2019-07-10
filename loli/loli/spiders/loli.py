import json
import re

import requests
import scrapy

from loli.items import LoliItem
from scipy.constants.constants import year


class loliSpider(scrapy.Spider):
    name = 'loli'
    start_urls = ['https://lol.qq.com/biz/hero/champion.js']
    
    def parse(self, response):
        
        #print(response.text)
        data = response.text
        json1 = re.findall(r"LOLherojs.champion=(.+?);", data)
        #print(json1[0])
        all_hero = json.loads(json1[0])['keys']
        #print(all_hero)
        all_hero_url = []
        for key,value in all_hero.items():
            url = 'https://lol.qq.com/biz/hero/' + value + '.js'
            #print(value)
            #all_hero_url.append(url)
            yield scrapy.Request(url = url,callback=self.parse_detail,meta={'hero':value})
            
    def parse_detail(self,response):
        #print(response.url)
        
        data = response.text
        value = response.meta['hero']
        #print(value)
        #deleteinfo = 'LOLherojs.champion.'+str(value)
        json1 = re.findall(r"LOLherojs.champion." + str(value) + "=(.+?);", data)
        #print(json1)
        hero_json = json.loads(json1[0])['data']
        #print(hero_json)
        hero_name = hero_json['name']
        #print(name)
        #print(hero_json['skins'])
        hero_skins = hero_json['skins']
        #print(hero_skins.items())
        item = LoliItem()
        for skin in hero_skins:
            id = skin['id']
            item['id'] = skin['id']
            skin_name = skin['name']
            if skin_name == 'default':
                skin_name = '默认皮肤'
            else:
                skin_name = skin_name
            item['skin_name'] = skin_name
            url = 'http://ossweb-img.qq.com/images/lol/web201310/skin/small'+str(id)+'.jpg'
            item['imageurl'] = url
            item['image_url'] = [item['imageurl']]
            item['hero_name'] = hero_name
            #print(hero_name,id,skin_name,url)    
            yield item
            
        
        #json1 = 

    
    
        
        