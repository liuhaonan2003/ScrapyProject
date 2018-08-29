# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from jdallsort.db.dbhelper import *
from jdallsort import const
import json

class JdallsortPipeline(object):
    def process_item(self, item, spider):
        print('JdallsortPipeline---------------------------liu')
        db = DBHelper()
        cate1_len = db.findKeySql(const.COUNT, table="jdallsort", params={"p_id":'0', "name":str(item['cate1'])})
        if int(cate1_len) == 0:
            cate1_id = db.findKeySql(const.INSERT, table="jdallsort", data={
                                                               "name":item["cate1"],
                                                               "p_id":0
                                                               })
            cate2_id = db.findKeySql(const.INSERT, table="jdallsort", data={
                                                               "name":item["cate2"],
                                                               "p_id":cate1_id
                                                               })
            for cate3 in item["cate3"]:
                cate3_id = db.findKeySql(const.INSERT, table="jdallsort", data={
                                                               "name":cate3,
                                                               "p_id":cate2_id
                                                               })
        else:
            print('else---------------------------------------liu')
            res_cate1 = db.findKeySql(const.FIND_BY_SQL, sql="select id from jdallsort", params={"p_id": '0',"name":str(item['cate1'])}, limit=1)
            cate2_id = db.findKeySql(const.INSERT, table="jdallsort", data={
                                                               "name":item["cate2"],
                                                               "p_id":res_cate1[0]['id']
                                                               })
            for cate3 in item["cate3"]:
                cate3_id = db.findKeySql(const.INSERT, table="jdallsort", data={
                                                               "name":cate3,
                                                               "p_id":cate2_id
                                                               })
        db.close()
        return item
