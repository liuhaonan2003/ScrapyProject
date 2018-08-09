# -*- coding: utf-8 -*-
#python3 -m scrapy crawl phone

import scrapy
from scrapy.http import Request
from jd.items import JdPhoneItem
import re
import urllib.request
 
class PhoneSpider(scrapy.Spider):
    name = "phone"
    allowed_domains = ["jd.com"]
    start_urls = ['http://jd.com/']
 
    #获取商品手机100页网址
    def parse(self, response):
        for i in range(1, 100):
            url = "https://search.jd.com/Search?keyword=手机&enc=utf-8&page="+str(i*2-1)
            print(url)
            yield Request(url=url,callback=self.product_url)
 
    #获取每页商品链接
    def product_url(self, response):
        urls = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
        for i in urls:
            url = response.urljoin(i)
            yield Request(url=url, callback=self.product)
 
    #获取商品的链接，名称，价格，评论数
    def product(self, response):
        #获取标题
        #title = response.xpath("//li[@class='img-hover']/img/@alt").extract()#部分网页不行
        
        product_title_tmp = response.xpath("//div[@class='sku-name']/text()").extract()
        #print(product_title)
        product_title = product_title_tmp[0].strip()
        if not product_title.strip():
            product_title = product_title_tmp[1].strip()
        title = response.xpath("//img/@alt").extract()
        #获取id号，用来构造价格和评论的链接
        pattern = r"(\d+)\.html$"
        id = re.findall(pattern, response.url)
        #得到价格
        priceUrl = "https://p.3.cn/prices/mgets?&skuIds=J_"+str(id[0])
        priceData = urllib.request.urlopen(priceUrl).read().decode("utf-8", "ignore")
        patt = r'"p":"(\d+\.\d+)"'
        price = re.findall(patt, priceData)
        #得到评论数
        commentUrl = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="+str(id[0])
        commentData = urllib.request.urlopen(commentUrl).read().decode("utf-8", "ignore")
        patt1 = r'"CommentCount":(\d+),'
        comment = re.findall(patt1, commentData)
 
        item = JdPhoneItem()
        item["url"] = response.url
        item["product_title"] = product_title
        item["title"] = title[0]
        item["price"] = price[0]
        item["comment"] = comment[0]
        yield item