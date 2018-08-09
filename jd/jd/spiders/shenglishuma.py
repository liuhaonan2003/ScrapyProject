# -*- coding: utf-8 -*-
#python3 -m scrapy crawl shenglishuma

import scrapy
from scrapy.http import Request
from jd.items import JdShengLiShuMaItem
from scrapy.selector import Selector
import re
import urllib.request
from selenium import webdriver
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))

class ShenglishumaSpider(scrapy.Spider):
    name = "shenglishuma"
    #allowed_domains = ["mall.jd.com"]
    #start_urls = ['https://mall.jd.com/view_search-907417-760070-755598-0-0-0-0-1-1-60.html']
    #start_urls = ['https://mall.jd.com/index-755598.html']
    #https://mall.jd.com/index-755598.html 数码店
    #start_urls = ['https://search.jd.com/Search?keyword=盛力数码专营店&enc=utf-8&suggest=1.def.0.V12&wq=shenglishuma&pvid=e6f52828f5084843b90dc45702d44e24']
    #https://mall.jd.com/index-764567.html 教育店
    #start_urls = ['https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=盛力电子教育专营店&sid=764567&stock=1&page=1&s=1&click=0']
    #https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&pvid=1c1f11553f444632ae6f1adaf3b44355
    #https://mall.jd.com/index-803447.html 美妆店
    #start_urls = ['https://search.jd.com/Search?keyword=片仔癀美妆旗舰店&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=片仔癀美妆旗舰店&sid=803447&stock=1&page=1&s=1&click=0']
    
#    allowed_domains = ["jd.com"]
#    start_urls = ['http://jd.com/']


 
    def __init__(self):
        display.start()
        self.browser = webdriver.Firefox()
        #self.browser.set_page_load_timeout(30)
        

    def closed(self,spider):
        print("spider closed")
        self.browser.close()
        display.stop()

    def start_requests(self):
#        start_urls = ['https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&wq=盛力电子教育专营店&pvid=1c1f11553f444632ae6f1adaf3b44355'.format(str(i)) for i in range(1,2,2)]
        #https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&sid=764567&stock=1&page=1&s=1&click=0
        #https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&sid=764567&stock=1&page=3&s=1&click=0
#        url_list = []
#        for i in range(1,3):
#            print(i)
#            url_list.append("https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&sid=764567&stock=1&page="+format(str(i))+"&s=1&click=0")
#            
#        for url in url_list:
#            yield Request(url=url, callback=self.parse)   
        for i in range(1, 100):
            url = "https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&page="+str(i*2-1)
            print(url)
            yield Request(url=url,callback=self.parse)
#        print(url_list)
#        start_urls = ['https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&sid=764567&stock=1&page=1&s=1&click=0','https://search.jd.com/Search?keyword=盛力电子教育专营店&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&sid=764567&stock=1&page=3&s=1&click=0']
#        for url in start_urls:
#            yield Request(url=url, callback=self.parse)

    #获取商品手机100页网址
    def parse(self, response):
        #urls = response.css(".userDefinedArea img::attr(src)").extract()
        #urls = response.css(".j-module a::attr(href)").extract()
        #urls = response.xpath('//div[@class="jPic"]/a[@target="_blank"]/@href').extract()
        #urls = response.xpath('/html/body/div[@class="layout-container"]/*/div[3]/*/div[@class="jPic"]').extract()       
        #/div[@class="d-layout-row d-clearfix jCurrent"]/div[@class="J_LayoutArea d-layout jCurrent"]/div[@class="fn-clear jSearchList-792077 jCurrent"]/div[@class="mc jCurrent"]
        #urls = response.xpath('//div[@id="96376278"]').extract()
        #urls = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
        urls = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
        print(urls)
        for i in urls:
            url = response.urljoin(i)
            print(url)
#            try:
            #yield Request(url=url, callback=self.product)
#            except Exception as err:
#                yield Request(url=url, callback=self.parse)
#        sel=Selector(response)
#        htmls=sel.xpath('/html/body/div[@class="layout-container"]/*/div[3]/')
#        print(htmls)
#        for ht in htmls:
#            print(ht)
        
        #urls = response.xpath('/html/body/title/text()').extract()
#        url = "https://search.jd.com/Search?keyword=%E7%9B%9B%E5%8A%9B%E6%95%B0%E7%A0%81%E4%B8%93%E8%90%A5%E5%BA%97&enc=utf-8&suggest=1.def.0.V12&wq=shenglishuma&pvid=e6f52828f5084843b90dc45702d44e24"
#        print(url)
#        yield Request(url=url,callback=self.product_url)
 
    #获取每页商品链接
#    def product_url(self, response):
#        urls = response.xpath('//div[@class="p-name p-name-type-2"]/a[@target="_blank"]/@href').extract()
#        for i in urls:
#            url = response.urljoin(i)
#            yield Request(url=url, callback=self.product)
 
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
#        pattern = r"(\d+)\.html$"
#        id = re.findall(pattern, response.url)
        
#        #得到价格
#        priceUrl = "https://p.3.cn/prices/mgets?&skuIds=J_"+str(id[0])
#        print(priceUrl)
#        priceData = urllib.request.urlopen(priceUrl).read().decode("utf-8", "ignore")
#        patt = r'"p":"(\d+\.\d+)"'
#        price = re.findall(patt, priceData)
#        #得到评论数
#        commentUrl = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds="+str(id[0])
#        commentData = urllib.request.urlopen(commentUrl).read().decode("utf-8", "ignore")
#        patt1 = r'"CommentCount":(\d+),'
#        comment = re.findall(patt1, commentData)
 
        item = JdShengLiShuMaItem()
        item["url"] = response.url
        item["product_title"] = product_title
        item["title"] = title[0]
#        item["price"] = price[0]
#        item["comment"] = comment[0]
        item["price"] = "100"
        item["comment"] = "100"
        yield item