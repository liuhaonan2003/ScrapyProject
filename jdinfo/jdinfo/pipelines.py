# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import pymysql.cursors
#from scrapy import Request
import scrapy
#import logging
import time
from jdinfo.db.dbhelper import *
from jdinfo import const
#from scrapy.pipelines.images import ImagesPipeline
#from scrapy.exceptions import DropItem

#logger = logging.getLogger('SaveImagePipeline')

class JdinfoPipeline(object):   
    def open_spider(self,spider):
        print('JdinfoPipeline--------------open_spider-------------liu')
        
    #mysql写入
    def process_item(self, item, spider):
        print('JdinfoPipeline---------------------------liu')
        self.db = DBHelper()
        t = int(time.time())
        self.db.findKeySql(const.UPDATE_BY_ATTR, table="jdlist",data={"state": 1}, params={"sn": item["sn"]})
        self.db.findKeySql(const.INSERT, table="jdinfo", data={
                                                               "sn":item["sn"],
                                                               "url":item["url"], 
                                                               "product_title": item["product_title"],
                                                               "title": item["title"], 
                                                               "category": item["category"], 
                                                               "price": item["price"], 
                                                               "comment": item["comment"],
                                                               "brank": item["brank"],
                                                               "property": item["property"],
                                                               "detail": item["detail"],
                                                               "detail_img": item["detail_img"],
                                                               "preview": item["preview"],
                                                               "preview_n0": item["preview_n0"],
                                                               "preview_n1": item["preview_n1"],
                                                               "preview_n2": item["preview_n2"],
                                                               "preview_n3": item["preview_n3"],
                                                               "preview_n4": item["preview_n4"],
                                                               "preview_n5": item["preview_n5"],
                                                               "preview_n6": item["preview_n6"],
                                                               "preview_n7": item["preview_n7"],
                                                               "preview_n8": item["preview_n8"],
                                                               "preview_n9": item["preview_n9"],
                                                               "ctime": t
                                                               })
        self.db.close()
        time.sleep(1)
        return item

#    #关闭连接
#    def close_spider(self):
#        self.db.close()