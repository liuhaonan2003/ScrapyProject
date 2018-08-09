# -*- coding: utf-8 -*-
#scrapy crawl TestA
import scrapy
from jd.items import AItem
class TestASpiders(scrapy.Spider):
    name='TestA'
    allowed_domains=['www.ejianyuntong.cn']
    start_urls=['http://www.ejianyuntong.com']
    def parse(self,response):
        item = AItem()
        hrefs = response.css(".s-list1 a::attr(href)").extract()
        pics = response.css(".s-list1 img::attr(src)").extract()
#        for href in hrefs:
#            print href
#        for pic in pics:
#            print pic
        for num in range(0,len(pics)):
#            print num
            pics[num]="http://haigoushangcheng.com"+pics[num]
#        print(pics)
        item['href'] = hrefs
        item['pic'] = pics
        yield item