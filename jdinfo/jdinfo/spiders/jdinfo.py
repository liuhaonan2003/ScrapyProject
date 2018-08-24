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
#import pickle
#import base64
from jdinfo.db.dbhelper import *
from jdinfo import const

#引入ActionChains类
from selenium.webdriver.common.action_chains import ActionChains

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
        #title = response.xpath("//img/@alt").extract()
        title = response.xpath("//div[@id='popbox']//h3/a/@title").extract()
        #print(title)
        #获取产品图片
        preview_list = response.xpath("//div[@id='spec-list']/ul/li/img/@src").extract()
        preview_imgzone = []
        preview_n0 = []
        preview_n1 = []
        preview_n2 = []
        preview_n3 = []
        preview_n4 = []
        preview_n5 = []
        preview_n6 = []
        preview_n7 = []
        preview_n8 = []
        preview_n9 = []
        for small in preview_list:
            print(small)
            preview_imgzone.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/imgzone/", small)))
            preview_n0.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n0/", small)))
            preview_n1.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n1/", small)))
            preview_n2.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n2/", small)))
            preview_n3.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n3/", small)))
            preview_n4.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n4/", small)))
            preview_n5.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n5/", small)))
            preview_n6.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n6/", small)))
            preview_n7.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n7/", small)))
            preview_n8.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n8/", small)))
            preview_n9.append(response.urljoin(re.sub(re.compile(r"/n[\d+]/", re.S), "/n9/", small)))
        time.sleep(1)
#        preview_list = response.xpath("//div[@id='spec-list']/ul/li/img/@src").extract()
#        preview_small = []
#        for small in preview_list:
#            preview_small.append(response.urljoin(small))
#        print(preview_small)
#        print(len(preview_small))
        #从商品图片放大图片处获取(涉及页面鼠标点击技术)
#        self.browser.get(response.url)
#        preview_middle = []
#        preview_large = []
#        for i in range(len(preview_small)):
#            look_move="//div[@id='spec-list']/ul/li["+str(i+1)+"]/img"
#            above = self.browser.find_element_by_xpath(look_move)
#            ActionChains(self.browser).context_click(above).perform()
#            html = self.browser.page_source
#            get_html = Selector(text=html)
#            preview = get_html.xpath("//img[@id='spec-img']/@src").extract()
#            preview_middle.append(response.urljoin(preview[0]))
#            preview = get_html.xpath("//img[@id='spec-img']/@jqimg").extract()
#            preview_large.append(response.urljoin(preview[0]))
#            time.sleep(1)
#        print(preview_middle)
#        print(preview_large)

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
        
        #获取分类
        category = response.xpath("//div[@id='crumb-wrap']//div[@class='crumb fl clearfix']//a/text()").extract()
        cate_arr = []
        cate_arr.append(category[0])
        cate_arr.append(category[1])
        cate_arr.append(category[2])
        cate_arr.append(category[3])
        #获取品牌
        brank = response.xpath("//ul[@id='parameter-brand']/li/@title").extract()
        #获取属性
        property = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/text()').re('.*：*.')
        property_arr = []
#        propertyStr = ''
        for property_li in property:
            tmp_li = property_li.split('：')
#            tmpStr = tmp_li[0] +':'+tmp_li[1]
#            propertyStr += "==="+tmpStr
            property_arr.append(tmp_li)
        #获取产品详情
        detail = response.xpath("//div[@id='detail']/div[@class='tab-con']").extract()
        #print(detail)
        #获取产品详情图片
        detail_imgs = response.xpath("//div[@id='detail']/div[@class='tab-con']//img//@src").extract()
        img_url = []
        for img in detail_imgs:
            # 注意imgurls是一个集合也就是多张图片
            tmp_url = response.urljoin(img)
            img_url.append(tmp_url)
        
        item = JdinfoItem()
        item["sn"] = str(id[0])
        item["url"] = response.url
        item["product_title"] = product_title
        #item["title"] = title[0]
        item["title"] = title
        item["category"] = json.dumps(cate_arr)
        item["price"] = price[0]
        item["comment"] = comment[0]
#        item["price"] = 0
#        item["comment"] = 0
        item["brank"] = brank[0].strip()
#        item["property"] = propertyStr
        item["property"] = json.dumps(property_arr)
        item['detail'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", str(detail))
        item['detail'] = re.sub(re.compile(r"//[^/]+?/", re.S), "/", item['detail'])
        item['detail'] = re.sub(re.compile(r'href=".*?"', re.S), 'href="#"', item['detail'])
        
        item['detail_img'] = json.dumps(img_url+preview_imgzone+preview_n0+preview_n1+preview_n2+preview_n3+preview_n4+preview_n5+preview_n6+preview_n7+preview_n8+preview_n9)
        item['preview'] = json.dumps(preview_imgzone)
        item['preview_n0'] = json.dumps(preview_n0)
        item['preview_n1'] = json.dumps(preview_n1)
        item['preview_n2'] = json.dumps(preview_n2)
        item['preview_n3'] = json.dumps(preview_n3)
        item['preview_n4'] = json.dumps(preview_n4)
        item['preview_n5'] = json.dumps(preview_n5)
        item['preview_n6'] = json.dumps(preview_n6)
        item['preview_n7'] = json.dumps(preview_n7)
        item['preview_n8'] = json.dumps(preview_n8)
        item['preview_n9'] = json.dumps(preview_n9)
        
        item['preview'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview'])
        item['preview_n0'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n0'])
        item['preview_n1'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n1'])
        item['preview_n2'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n2'])
        item['preview_n3'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n3'])
        item['preview_n4'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n4'])
        item['preview_n5'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n5'])
        item['preview_n6'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n6'])
        item['preview_n7'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n7'])
        item['preview_n8'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n8'])
        item['preview_n9'] = re.sub(re.compile(r"http[s]?://[^/]+?/", re.S), "/", item['preview_n9'])
        #print(item)
        yield item