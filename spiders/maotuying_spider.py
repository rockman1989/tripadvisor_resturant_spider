# -*- coding: utf-8 -*-
import scrapy
from maotuying_test.items import MaotuyingTestItem

class MaotuyingSpiderSpider(scrapy.Spider):
    name = 'maotuying_spider'
    allowed_domains = ['tripadvisor.cn']
    #start_urls = ['https://www.tripadvisor.cn/Restaurants-g308272-Shanghai.html']
    start_urls = ['https://www.tripadvisor.cn/Restaurants-g294211-China.html']
    def parse(self, response):
        #print(response.request.url)
        if '-oa' in response.request.url :
            url_list_2 = response.xpath("//ul[@class='geoList']/li/a/@href").extract()
            for i_item in url_list_2 :
                place_url_2 = 'https://www.tripadvisor.cn' + i_item
                yield scrapy.Request(place_url_2,callback=self.everyPlace)
            #翻页
            next_link_2 = response.xpath("//div[@class='pgLinks']/a[@class='guiArw sprite-pageNext ']/@href").extract()
            if next_link_2 :
                next_link_2 = next_link_2[0]
                yield scrapy.Request("https://www.tripadvisor.cn"+next_link_2,callback=self.parse)
            
        else :
            url_list = response.xpath("//div[@class='geo_image']//a/@href").extract()
            for i_item in url_list:
                place_url = 'https://www.tripadvisor.cn' + i_item
                yield scrapy.Request(place_url,callback=self.everyPlace)

            #翻页
            next_link = response.xpath("//div[@class='unified pagination ']/a/@href").extract()
            if next_link :
                next_link = next_link[0]
                yield scrapy.Request("https://www.tripadvisor.cn"+next_link,callback=self.parse)

    #每个地点
    def everyPlace(self, response):
        restaurant_list = response.xpath("//div[@id='EATERY_SEARCH_RESULTS']//div[@class='title']/a/@href").extract()
        for i_item in restaurant_list:
            restaurant_url = 'https://www.tripadvisor.cn' + i_item
            yield scrapy.Request(restaurant_url,callback=self.restaurant_info)
        #翻页
        next_link = response.xpath("//div[@class='unified pagination js_pageLinks']/a/@href").extract()
        if next_link :
            next_link = next_link[0]
            yield scrapy.Request("https://www.tripadvisor.cn"+next_link,callback=self.parse)
        

    #每个餐厅
    def restaurant_info(self, response):
        maotuying_item = MaotuyingTestItem()
        maotuying_item['restaurant_name'] = response.xpath("//div[@id='atf_header']/div[@id='taplc_resp_rr_top_info_rr_resp_0']//h1/text()").extract_first()
        maotuying_item['restaurant_rank'] = response.xpath("//div[@class='popIndexContainer']//b/span/text()").extract_first()
        maotuying_item['restaurant_evaluate'] = response.xpath("//div[@class='restaurants-detail-overview-cards-RatingsOverviewCard__primaryRatingRow--VhEsu']/a/text()").extract_first()
        maotuying_item['restaurant_addr'] = response.xpath("//div[@class='restaurants-detail-overview-cards-LocationOverviewCard__addressLink--1pLK4 restaurants-detail-overview-cards-LocationOverviewCard__detailLink--iyzJI']//div[@class='ui_link']/span/text()").extract_first()
        maotuying_item['restaurant_phone'] = response.xpath("//div[@class='blEntry phone']//span/text()").extract_first()
        maotuying_item['restaurant_pic_num'] = response.xpath("//span[@class='see_all_count']//span[@class='details']/text()").extract_first()
        
        new_list=response.xpath("//div[@class='restaurants-detail-overview-cards-DetailsSectionOverviewCard__detailsSummary--evhlS']/div")

        for item in new_list:
            theme = item.xpath('.//div/text()').extract()[0]
            if '美食' in theme :
                maotuying_item['restaurant_food_tpye'] = item.xpath(".//div/text()").extract()[1]
            #elif '特殊饮食' in theme :
                #maotuying_item['restaurant_special'] = item.xpath(".//div/text()").extract()[1]
            #elif '餐时' in theme :
                #maotuying_item['restaurant_time'] = item.xpath(".//div/text()").extract()[1]
        yield maotuying_item
        print(maotuying_item)
