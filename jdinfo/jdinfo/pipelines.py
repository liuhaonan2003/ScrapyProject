# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import pymysql.cursors
#from scrapy import Request
import scrapy
import logging
import time
from jdinfo.db.dbhelper import *
from jdinfo import const
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

logger = logging.getLogger('SaveImagePipeline')

class JdinfoPipeline(object):   
    def open_spider(self,spider):
        self.db = DBHelper()
        
    #mysql写入
    def process_item(self, item, spider):
        print('JdinfoPipeline---------------------------liu')
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
        time.sleep(1)
        return item

    #关闭连接
    def close_spider(self):
        self.db.close()
        
class SaveImagePipeline(ImagesPipeline):

    """
            下载图片
    """
    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for image_url in item['imgurl']:
            print('SaveImagePipeline------------------------liu')
            print(image_url)
            yield scrapy.Request(url=image_url)
            

    def item_completed(self, results, item, info):
        """
                            文件下载完成之后，返回一个列表 results
                            列表中是一个元组，第一个值是布尔值，请求成功会失败，第二个值的下载到的资源
        """
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('下载失败')
        item['image_paths'] = image_paths
        # 打印日志
        logger.debug('下载图片成功')
        return item 

    def file_path(self, request, response=None, info=None):
        """
                            返回文件名
        """
        return request.url.split('/')[-1]

    # def file_path(self, request, response=None, info=None):
    #     # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    #     image_guid = request.url.split('/')[-1]  # 提取url前面名称作为图片名。
    #     return image_guid