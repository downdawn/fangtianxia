# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtianxiaItem(scrapy.Item):
    # define the fields for your item here like:
    collection = 'rent'  # 数据库表

    province = scrapy.Field()  # 省份
    city_name = scrapy.Field()  # 城市
    url = scrapy.Field()  # 详情页地址
    house_price = scrapy.Field()  # 房源价格
    price_unit = scrapy.Field()  # 价格单位
    house_way = scrapy.Field()  # 房源简介
    house_ad = scrapy.Field()  # 招租广告
    Community_name = scrapy.Field()  # 小区名称
    house_addres = scrapy.Field()  # 房源地址
    house_master = scrapy.Field()  # 联系人名字
    house_phone = scrapy.Field()  # 联系人电话
    # house_describe = scrapy.Field()  # 房源描述
    # house_facility = scrapy.Field()  # 配套设施
    area_name = scrapy.Field()  # 区域


