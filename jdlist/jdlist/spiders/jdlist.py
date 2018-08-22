# -*- coding: utf-8 -*-
#python3 -m scrapy crawl shenglishuma

import scrapy
from scrapy.http import Request
from jdlist.items import JdlistItem
from scrapy.selector import Selector
import re
#import urllib.request
from selenium import webdriver
from pyvirtualdisplay import Display
import time
import json
display = Display(visible=0, size=(800, 600))

class JdlistSpider(scrapy.Spider):
    name = "jdlist"
    allowed_domains = ["jd.com"]
    start_urls = ['http://jd.com/']

    def __init__(self):
        display.start()
        SERVICE_ARGS = ['--load-images=false', '--disk-cache=true', '--ignore-ssl-errors=true']
        self.browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        self.browser.set_page_load_timeout(300)
        

    def closed(self,spider):
        print("spider closed")
        self.browser.close()
        display.stop()

    def start_requests(self):
        input_text = input("请输入你要抓取的内容：\n")
        keyword = str(input_text)
        for i in range(1, 100):
            url = "https://search.jd.com/Search?keyword="+keyword+"&enc=utf-8&page="+str(i*2-1)
            #url = "https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&page="+str(i*2-1)
            yield Request(url=url,meta={'keyword': keyword},callback=self.parse)

    #获取商品手机100页网址
    def parse(self, response):
        keyword = response.meta['keyword']
        urls = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
        list = []
        for i in urls:
            url1 = response.urljoin(i)
            list.append(url1)
        item = JdlistItem()
        item["keyword"] = keyword
        item["url"] = list
        yield item