# -*- coding: utf-8 -*-
#python3 -m scrapy crawl shenglishuma
import scrapy
from jdpicdownload.items import JdpicdownloadItem
import json
from jdpicdownload.db.dbhelper import *
from jdpicdownload import const

class JdpicdownloadSpider(scrapy.Spider):
    name = 'jdpicdownload'
    allowed_domains = ['jd.com']
    start_urls = ['http://jd.com/']
    
    def parse(self, response):
        db = DBHelper()
        res = db.findKeySql(const.FIND_BY_SQL, sql="select * from jdinfo", params={"img_state": 0}, limit=40)
        db.close()
        total = len(res)
        count = 0
        
        for info in res:
            item = JdpicdownloadItem()
            count = count + 1
            print('数据爬取中：%d/%d' %(total-count,total))
            item["sn"] = str(info['sn'])
            item['detail_img'] = json.loads(info['detail_img'])
            yield item