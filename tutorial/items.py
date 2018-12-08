# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BaiDuSearchItem(scrapy.Item):
    visit_url = scrapy.Field()  # 链接
    page = scrapy.Field()  # 页码
    rank = scrapy.Field()  # 第几位
    title = scrapy.Field()  # 主标题


class QQVideoCommentItem(scrapy.Item):
    comment = scrapy.Field()  # 图片的链接

class ProxyItem(scrapy.Item):
    ip = scrapy.Field()  # IP
    port = scrapy.Field()  # port
    type = scrapy.Field()  # 匿名度
    schemes = scrapy.Field()  # IP类型
    addr = scrapy.Field()  # 地址
    speed = scrapy.Field()  # 速度
    update = scrapy.Field()  # 更新时间
    ori = scrapy.Field()  # 来源
