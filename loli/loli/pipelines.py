# -*- coding: utf-8 -*-
import pymongo
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem


#from scrapy.signals import spider_closed
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
class LoliPipeline(object):
    def process_item(self, item, spider):
        return item


class MONGOPipeline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
           )
            
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
    def close_spider(self,spider):
        self.client.close()
        
    def process_item(self,item,spider):
        #self.db[item.table_name].insert(dict(item))
        self.db[item.table_name].update({'id':item.get('id')},{'set':dict(item)},True)
        return item
        
        
class lolimagePipeline(ImagesPipeline): 
    def get_media_requests(self, item, info):
        for url in item['image_url']:
            yield scrapy.Request(url,meta={'hero_name':item['hero_name'],'skin_name':item['skin_name']})
            
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok,x in results if ok]
        if not image_paths:
            raise DropItem('没有图片')
        item['image_paths'] = image_paths
        return item
    
    def file_path(self, request, response=None, info=None):
        hero_name = request.meta['hero_name']
        skin_name = request.meta['skin_name']
        if  skin_name.find('/') == -1:
            pass
        else:
            skin_name = skin_name.replace('/', '／')
        skin_name = skin_name + '.jpg'
        filename = '{0}/{1}'.format(hero_name,skin_name)
        return filename
        
        
        