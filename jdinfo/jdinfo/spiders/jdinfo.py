# -*- coding: utf-8 -*-
#python3 -m scrapy crawl shenglishuma

import scrapy
from scrapy.http import Request
from jdinfo.items import JdinfoItem
from jdinfo.pipelines import JdinfoPipeline
from scrapy.selector import Selector
import re
import urllib.request
from selenium import webdriver
from pyvirtualdisplay import Display
import time
import json
from jdinfo.db.dbhelper import *
from jdinfo import const
display = Display(visible=0, size=(800, 600))

class JdinfoSpider(scrapy.Spider):
    name = "jdinfo"
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
        print('开始爬取详情页')
        db = DBHelper()
        res = db.findKeySql(const.FIND_BY_SQL, sql="select * from jdlist", params={"state": 0}, limit=0)
        db.close()
        total = len(res)
        count = 0
        for info in res:
            count = count + 1
            print('数据爬取中：%d/%d' %(total-count,total))
            yield Request(url=info['url'],callback=self.parse)

    #获取商品的链接，名称，价格，评论数
    def parse(self, response):
        #获取标题
        #title = response.xpath("//li[@class='img-hover']/img/@alt").extract()#部分网页不行
#        print(response.url)
        product_title_tmp = response.xpath("//div[@class='sku-name']/text()").extract()
#        print(product_title_tmp)
        product_title = product_title_tmp[0].strip()
        if not product_title.strip():
            product_title = product_title_tmp[1].strip()
        title = response.xpath("//img/@alt").extract()
#        print(title[0])
        #获取id号，用来构造价格和评论的链接
        pattern = r"(\d+)\.html$"
        id = re.findall(pattern, response.url)
        
        #得到价格
        priceUrl = "https://p.3.cn/prices/mgets?&skuIds=J_"+str(id[0])
#        print(priceUrl)
        priceData = urllib.request.urlopen(priceUrl).read().decode("utf-8", "ignore")
        patt = r'"p":"(\d+\.\d+)"'
        price = re.findall(patt, priceData)
        #得到评论数
        commentUrl = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="+str(id[0])
        commentData = urllib.request.urlopen(commentUrl).read().decode("utf-8", "ignore")
        patt1 = r'"CommentCount":(\d+),'
        comment = re.findall(patt1, commentData)
        
        brank = response.xpath("//ul[@id='parameter-brand']/li/@title").extract()
        
        item = JdinfoItem()
        item["url"] = response.url
        item["product_title"] = product_title
        item["title"] = title[0]
        item["price"] = price[0]
        item["comment"] = comment[0]
        item["brank"] = brank[0].strip()
        print(item)
        yield item