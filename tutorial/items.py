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
    comment = scrapy.Field()  # 评论

class ProxyItem(scrapy.Item):
    ip = scrapy.Field()  # IP
    port = scrapy.Field()  # port
    type = scrapy.Field()  # 匿名度
    schemes = scrapy.Field()  # IP类型
    addr = scrapy.Field()  # 地址
    speed = scrapy.Field()  # 速度
    update = scrapy.Field()  # 更新时间
    ori = scrapy.Field()  # 来源

class CSDN2018BlogStarItem(scrapy.Item):
    link = scrapy.Field()  # 博客地址
    blog_title = scrapy.Field()  # 标题
    description = scrapy.Field()  # 描述
    avatar_pic = scrapy.Field()  # 头像
    original = scrapy.Field()  # 原创
    fans = scrapy.Field()  # 粉丝
    star = scrapy.Field()  # 喜欢
    comment = scrapy.Field()  # 评论
    level = scrapy.Field()  # 等级
    visit = scrapy.Field()  # 访问
    score = scrapy.Field()  # 积分
    rank = scrapy.Field()  # 排名
    medal = scrapy.Field()  # 勋章
    archives = scrapy.Field()  # 归档
    blogstar_comment = scrapy.Field()  # 作者博客之星活动的评论

class BlogStar2018Item(scrapy.Item):
    link = scrapy.Field()  # 博客地址
    blog_title = scrapy.Field()  # 标题
    description = scrapy.Field()  # 描述
    avatar_pic = scrapy.Field()  # 头像
    original = scrapy.Field()  # 原创
    fans = scrapy.Field()  # 粉丝
    star = scrapy.Field()  # 喜欢
    comment = scrapy.Field()  # 评论
    level = scrapy.Field()  # 等级
    visit = scrapy.Field()  # 访问
    score = scrapy.Field()  # 积分
    rank = scrapy.Field()  # 排名
    medal = scrapy.Field()  # 勋章
    colunms = scrapy.Field()  # 专栏
    blogstar_vote = scrapy.Field()  # 作者博客之星活动的投票信息

