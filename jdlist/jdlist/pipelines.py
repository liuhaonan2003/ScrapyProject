# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql.cursors
from scrapy import Request
import time
import re

class JdlistPipeline(object):
    """
    1、连接数据库操作
    """
    def __init__(self,host,port,user,passwd,charset,db):
        '''
                            初始化mysql数据的主机、端口号、数据库名称，帐户，密码，编码
        :param host:
        :param port:
        :param user:
        :param passwd:
        :param charset:
        :param db:
        '''
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.db = db
 
    @classmethod
    def from_crawler(cls,crawler):
        """
        1、读取settings里面的mysql数据的host、port、user、passwd、charset、db。
        :param crawler:
        :return:
        """
        return cls(
            host = crawler.settings.get("MYSQL_HOST"),
            port = crawler.settings.get("MYSQL_PORT"),
            user = crawler.settings.get("MYSQL_USER"),
            passwd = crawler.settings.get("MYSQL_PASSWD"),
            charset = crawler.settings.get("MYSQL_CHARSET"),
            db = crawler.settings.get("MYSQL_DB")
        )
        
        
    def open_spider(self,spider):
        self.conn=pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  charset=self.charset,
                                  cursorclass=pymysql.cursors.DictCursor)
        cur = self.conn.cursor()
        cur.execute("USE "+self.db)
    #mysql写入
    def process_item(self, item, spider):
        '''
        1、将数据写入数据库
        :param item:
        :param spider:
        :return:
        '''
        try:
            
            sql = ""
            print('============================JdlistPipeline start===============================')
            t = int(time.time())
            for url in item["url"]:
                #print(t)
                pattern = r"(\d+)\.html$"
                sn = re.findall(pattern, url)
#                print(url)
                sql += "('"+sn[0]+"','"+url+"',"+format(t)+"),"
#                sql += "('"+url+"'),"
            print(sql)
            if not sql.strip():
                print('sql is null')
            else:    
                sql = "INSERT INTO jdlist (sn,url,ctime) VALUES "+sql[0:len(sql)-1]
#                sql = "INSERT INTO jdlist (url) VALUES "+sql[0:len(sql)-1]
                print(sql)
                cur = self.conn.cursor()
                cur.execute(sql)
                self.conn.commit()
            
            print('============================JdlistPipeline end===============================')
#            url = item["url"]
#            print('JdlistPipeline')
#            print(url)
#            cur = self.conn.cursor()
#            #sql = "INSERT INTO jdlist (url) VALUES ('"+url+"')"
#            sql = "REPLACE INTO jdlist (url) VALUES ('"+url+"')"
#            cur.execute(sql)
#            self.conn.commit()
            return item
        except Exception as err:
            print(err)
 
    #关闭连接
    def close_spider(self):
        '''
        1、关闭数据库连接
        :param spider:
        :return:
        '''
        self.conn.close()
