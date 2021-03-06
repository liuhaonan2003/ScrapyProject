# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem
import time
from jdpicdownload.db.dbhelper import *
from jdpicdownload import const

class ImagespiderPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for url in item['detail_img']:
            yield Request(url,meta={'name':item['sn']})

    def file_path(self, request, response=None, info=None):
         # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
#         image_guid = request.url.split('/')[-1]  # 提取url前面名称作为图片名。
#         name = request.meta['name']
#         name = re.sub(r'[？\\*|“<>:/]', '', name)
         filename = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "", request.url)#u'{0}/{1}'.format(name, image_guid)
         return filename
    
    def item_completed(self, results, item, info):
        print('item_completed------------------------liu')
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['detail_img'] = image_paths
        #time.sleep(1)
        return item

class JdpicdownloadPipeline(object):   
    def open_spider(self,spider):
        print('open_spider-----------JdpicdownloadPipeline----------------liu')
    #mysql写入
    def process_item(self, item, spider):
        self.db = DBHelper()
        print('JdpicdownloadPipeline---------------------------liu')
        print(item)
        t = int(time.time())
        self.db.findKeySql(const.UPDATE_BY_ATTR, table="jdinfo",data={
                                                                      "img_state": 1,
                                                                      "utime": t
                                                                      }, params={"sn": item["sn"]})
        self.db.close()
        time.sleep(2)
        return item

#    #关闭连接
#    def close_spider(self):
#        self.db.close()