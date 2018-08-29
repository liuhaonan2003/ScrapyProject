# -*- coding: utf-8 -*-
#python3 -m scrapy crawl shenglishuma
import scrapy
from scrapy.http import Request
from jdallsort.items import JdallsortItem
import json
from scrapy.selector import Selector
import re
#from jdallsort.db.dbhelper import *
#from jdallsort import const

class JdallsortSpider(scrapy.Spider):
    name = 'jdallsort'
    allowed_domains = ['jd.com']
    start_urls = ['https://www.jd.com/allSort.aspx']
    
    def parse(self, response):
        """获取分类页"""
        try:
            cate_html = response.xpath('//div[@class="category-item m"]').extract()
            total = len(cate_html)
            count = 0
            for chtml in cate_html:
                print('=================================start======================================')
                count = count + 1
                print('数据爬取中：%d/%d' %(total-count,total))
                #cate1 = re.findall(r'<h2 class="item-title">(.*)</h2>', chtml)
                sel = Selector(text=chtml, type="html")
                cate1 = sel.xpath('//div[@class="category-item m"]/div[@class="mt"]/h2[@class="item-title"]/span/text()').extract()
                #print(cate1)
                cate2_html = sel.xpath('//div[@class="category-item m"]/div[@class="mc"]/div[@class="items"]/dl').extract()
                for c2html in cate2_html:
                    sel1 = Selector(text=c2html, type="html")
                    cate2 = sel1.xpath('//dl/dt/a/text()').extract()
                    #print(cate2)
                    cate3 = sel1.xpath('//dl/dd/a/text()').extract()
                    #print(cate3)
                    item = JdallsortItem()
                    item['cate1'] = str(cate1[0])
                    item['cate2'] = str(cate2[0])
                    item['cate3'] = cate3
                    #print(item)
                    yield item
                print('=================================end======================================')
        except Exception as e:
            print('error:', e)