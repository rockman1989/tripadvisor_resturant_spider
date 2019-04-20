# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaotuyingTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #餐厅排名
    restaurant_rank = scrapy.Field();
    #餐厅名称
    restaurant_name = scrapy.Field();
    #餐厅点评数
    restaurant_evaluate = scrapy.Field();
    #餐厅地址
    restaurant_addr = scrapy.Field();
    #餐厅电话
    restaurant_phone = scrapy.Field();
    #照片张数
    restaurant_pic_num = scrapy.Field();
    #美食类型
    restaurant_food_tpye = scrapy.Field();
    #特殊饮食
    restaurant_special = scrapy.Field();
    #餐食
    restaurant_time = scrapy.Field();