# -*- coding: utf-8 -*-
import pymysql
from maotuying_test import settings
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MaotuyingTestPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()


    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into restaurant(restaurant_rank,
                restaurant_name,restaurant_evaluate,restaurant_addr,restaurant_phone,restaurant_pic_num,restaurant_food_tpye
                )
                value(%s,%s,%s,%s,%s,%s,%s)""",
                (item['restaurant_rank'],
                 item['restaurant_name'],
                 item['restaurant_evaluate'],
                 item['restaurant_addr'],
                 item['restaurant_phone'],
                 item['restaurant_pic_num'],
                 item['restaurant_food_tpye']
                 #item['restaurant_special'],
                 #item['restaurant_time']))
                 ))
            self.connect.commit()
        except Exception as err:
            print("重复插入了==》错误信息：" + str(err))

        return item
