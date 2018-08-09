# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#scrapy crawl TestJd
import pymysql.cursors
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request

class JdPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for image_url in item['imgurl']:
            yield Request(image_url)

    # def file_path(self, request, response=None, info=None):
    #     # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    #     image_guid = request.url.split('/')[-1]  # 提取url前面名称作为图片名。
    #     return image_guid
class APipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # 循环每一张图片地址下载，若传过来的不是集合则无需循环直接yield
        for img_url in item['pic']:
            yield Request(img_url)
        for href_url in item['href']:
            print(href_url)
    # def file_path(self, request, response=None, info=None):
    #     # 重命名，若不重写这函数，图片名为哈希，就是一串乱七八糟的名字
    #     image_guid = request.url.split('/')[-1]  # 提取url前面名称作为图片名。
    #     return image_guid
    
class JdPhonePipeline(object):
    #连接登陆mysql，新建数据表
    def __init__(self):
        self.conn=pymysql.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="Tx@2018@2021@F1@com",
                                  charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)
        cur = self.conn.cursor()
        cur.execute("CREATE DATABASE jd")
        cur.execute("USE jd")
        cur.execute("CREATE TABLE phone (id INT PRIMARY KEY AUTO_INCREMENT,url VARCHAR(50),product_title VARCHAR(255),title VARCHAR(50),price VARCHAR(10),comment VARCHAR(10))")
 
    #mysql写入
    def process_item(self, item, spider):
        try:
            url = item["url"]
            product_title = item["product_title"]
            title = item["title"]
            price = item["price"]
            comment = item["comment"]
#            print(url)
            cur = self.conn.cursor()
            sql = "INSERT INTO phone (url, product_title, title, price, comment) VALUES ('"+url+"','"+product_title+"','"+title+"','"+price+"','"+comment+"')"
            cur.execute(sql)
            self.conn.commit()
            return item
        except Exception as err:
            print(err)
 
    #关闭连接
    def close_spider(self):
        self.conn.close()
        
class JdShengLiShuMaPipeline(object):
    #连接登陆mysql，新建数据表
    def __init__(self):
        self.conn=pymysql.connect(host="127.0.0.1",
                                  user="root",
                                  passwd="Tx@2018@2021@F1@com",
                                  charset='utf8',
                                  cursorclass=pymysql.cursors.DictCursor)
        cur = self.conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS `jd`")
        cur.execute("CREATE DATABASE jd")
        cur.execute("USE jd")
        cur.execute("DROP TABLE IF EXISTS `phone`")
        cur.execute("CREATE TABLE phone (id INT PRIMARY KEY AUTO_INCREMENT,url VARCHAR(50),product_title VARCHAR(255),title VARCHAR(50),price VARCHAR(10),comment VARCHAR(10))")
 
    #mysql写入
    def process_item(self, item, spider):
        try:
            url = item["url"]
            product_title = item["product_title"]
            title = item["title"]
            price = item["price"]
            comment = item["comment"]
            print(url)
            cur = self.conn.cursor()
            sql = "INSERT INTO phone (url, product_title, title, price, comment) VALUES ('"+url+"','"+product_title+"','"+title+"','"+price+"','"+comment+"')"
            cur.execute(sql)
            self.conn.commit()
            return item
        except Exception as err:
            print(err)
 
    #关闭连接
    def close_spider(self):
        self.conn.close()