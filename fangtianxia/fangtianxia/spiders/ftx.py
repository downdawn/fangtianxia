# -*- coding: utf-8 -*-
import scrapy
from fangtianxia.items import FangtianxiaItem
from urllib.parse import urljoin
import re
from copy import deepcopy


class FtxSpider(scrapy.Spider):
    name = 'ftx'
    allowed_domains = ['fang.com']
    start_urls = ['https://sh.zu.fang.com/cities.aspx']

    def parse(self, response):  # 获取每个城市url
        item = FangtianxiaItem()
        li_list = response.xpath("//div[@class='outCont']//li")
        for li in li_list:
            item["province"] = li.xpath("./a[1]/preceding-sibling::*/text()").extract_first()
            city_list = li.xpath("./a")
            for city in city_list:
                item["city_name"] = city.xpath("./text()").extract_first()
                city_link = city.xpath("./@href").extract_first()
                city_link = urljoin(response.url, city_link)
                print(city_link)
                yield scrapy.Request(
                    city_link,
                    callback=self.parse_city,
                    meta={"item": deepcopy(item)}
                )

    def parse_city(self, response):  # 获取每个城市各个区域的url
        item = response.meta["item"]
        area_url = response.xpath("//dl[@id='rentid_D04_01']//dd/a[contains(@class,'org')]/following-sibling::*/@href").extract()
        for area in area_url:
            area = urljoin(response.url, area)
            yield scrapy.Request(
                area,
                callback=self.parse_url,
                meta={"item": deepcopy(item)},
            )

    def parse_url(self, response):  # 获取房源详情页的url
        item = response.meta["item"]
        url_list = response.xpath("//div[@class='houseList']/dl/dt/a/@href").extract()
        for url in url_list:
            url = urljoin(response.url, url)
            yield scrapy.Request(
                url,
                callback=self.parse_house,
                meta={"item": item},
            )

        # 翻页
        url = response.xpath("//a[text()='下一页']/@href").extract_first()
        next_url = urljoin(response.url, url)
        if next_url is not None:
            yield scrapy.Request(
                next_url,
                callback=self.parse
            )

    def parse_house(self, response):  # 解析详情页
        item = response.meta["item"]
        item["url"] = response.url
        item["house_price"] = response.xpath("//div[contains(@class,'trl-item')]/i/text()").extract_first()
        house = ''.join(response.xpath("//div[contains(@class,'trl-item')]//text()").extract()).strip().split("\r\n")
        item["price_unit"] = re.sub(r'\d', '', house[0])
        item["house_way"] = response.xpath("//div[@class='tt']/text()").extract()
        item["house_ad"] = response.xpath("//div[contains(@class,'tab-cont')]/h1/text()").extract_first()
        item["Community_name"] = response.xpath("//div[contains(@class,'rcont')]/a/text()").extract_first()
        item["house_addres"] = response.xpath("//div[@class='rcont']/a/text()").extract_first()
        item["house_master"] = response.xpath("//span[@class='zf_mfname']/text()").extract_first()
        item["house_phone"] = response.xpath("//span[@class='zf_mftel']/text()").extract()
        # item["house_describe"] = response.xpath("//div[@class='cont yc ']/p/text()").extract_first()
        # item["house_facility"] = response.xpath("//div[@class='cont clearfix']/ul/li/text()").extract()
        item["area_name"] = response.xpath("//div[@class='bread']/a[3]/text()").extract_first()
        yield item

        # print(item)
