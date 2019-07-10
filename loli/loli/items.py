# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LoliItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    table_name = 'loli'
    
    hero_name = scrapy.Field()
    id = scrapy.Field()
    skin_name = scrapy.Field()
    imageurl = scrapy.Field()
    image_paths = scrapy.Field()
    image_url = scrapy.Field()
