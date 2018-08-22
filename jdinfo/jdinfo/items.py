# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdinfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sn = scrapy.Field()
    url = scrapy.Field()
    product_title = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()
    comment = scrapy.Field()
    brank = scrapy.Field()
    property = scrapy.Field()
    detail = scrapy.Field()
    
    detail_img = scrapy.Field()
    
    preview_n0 = scrapy.Field()
    preview_n1 = scrapy.Field()
    preview_n2 = scrapy.Field()
    preview_n3 = scrapy.Field()
    preview_n4 = scrapy.Field()
    preview_n5 = scrapy.Field()
    preview_n6 = scrapy.Field()
    preview_n7 = scrapy.Field()
    preview_n8 = scrapy.Field()
    preview_n9 = scrapy.Field()
#    print('JdinfoItem:\n')
#    print(url)
    pass