# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    imgurl = scrapy.Field()
    pass

class AItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pic = scrapy.Field()
    href = scrapy.Field()
    pass

class JdPhoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    product_title = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    comment = scrapy.Field()
    pass

class JdShengLiShuMaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    print('item:\n')
    print(url)
    product_title = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    comment = scrapy.Field()
    pass