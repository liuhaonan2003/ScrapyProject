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
        res = db.findKeySql(const.FIND_BY_SQL, sql="select * from jdinfo", params={"img_state": 0}, limit=0)
        db.close()
        total = len(res)
        count = 0
        item = JdpicdownloadItem()
        for info in res:
            count = count + 1
            print('数据爬取中：%d/%d' %(total-count,total))
            item["sn"] = info['sn']
            item['preview'] = json.loads(info['detail_img'])+json.loads(info['preview'])+json.loads(info['preview_n0'])+json.loads(info['preview_n1'])+json.loads(info['preview_n2'])+json.loads(info['preview_n3'])+json.loads(info['preview_n4'])+json.loads(info['preview_n5'])+json.loads(info['preview_n6'])+json.loads(info['preview_n7'])+json.loads(info['preview_n8'])+json.loads(info['preview_n9'])
            yield item