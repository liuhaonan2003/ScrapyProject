# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import pymysql.cursors
from scrapy import Request
import time
from jdinfo.db.dbhelper import *
from jdinfo import const

class JdinfoPipeline(object):   
    def open_spider(self,spider):
        self.db = DBHelper()
    #mysql写入
    def process_item(self, item, spider):
        print('JdinfoPipeline---------------------------liu')
        self.db.findKeySql(const.UPDATE_BY_ATTR, table="jdlist",data={"state": 1}, params={"url": item["url"]})
        self.db.findKeySql(const.INSERT, table="jdinfo", data={
                                                               "url":item["url"], 
                                                               "product_title": item["product_title"],
                                                               "title": item["title"], 
                                                               "price": item["price"], 
                                                               "comment": item["comment"]
                                                               })
        return item

    #关闭连接
    def close_spider(self):
        self.db.close()
