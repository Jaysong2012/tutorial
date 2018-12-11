# -*- coding: utf-8 -*-
import scrapy
import json
from tutorial.items import CSDN2018BlogStarItem

class Csdn2018BlogstarSpider(scrapy.Spider):
    name = 'csdn_2018_blogstar'
    allowed_domains = ['blog.csdn.net']
    start_urls = ['https://blog.csdn.net/blogdevteam/phoenix/comment/list/84874036?page={}&size=15&tree_type=1']

    user_set = set()

    def start_requests(self):
        #yield scrapy.Request('https://blog.csdn.net/blogdevteam', callback=lambda response, info=None: self.parse_blog_user_info(response,info))
        for url in self.start_urls:
            yield scrapy.Request(url.format(1), callback=self.parse)

    def parse(self, response):
        resp_dict = json.loads(response.text)
        if 'success' == resp_dict['content']:
            for comment in resp_dict['data']['list']:
                username = comment['info']['UserName'].lower()
                #截止时间为2018年12月11日 并且 附上自己的博客才算报名
                if comment['info']['Content'].find('csdn.net/'+username) > -1 and comment['info']['PostTime'] < '2018-12-11 00:00:00':
                    #喜欢重复刷评论的小哥哥,刷了多次也只算一次啊
                    if username not in __class__.user_set:
                        __class__.user_set.add(username)
                        #接下来到这里拉用户信息
                        yield scrapy.Request('https://blog.csdn.net/'+username, callback=lambda response, info=comment['info']: self.parse_blog_user_info(response,info))

            for page in range(2,resp_dict['data']['page_count']+1):
                yield scrapy.Request(self.start_urls[0].format(page), callback=self.parse_other_page)

    def parse_other_page(self,response):
        resp_dict = json.loads(response.text)
        if 'success' == resp_dict['content']:
            for comment in resp_dict['data']['list']:
                username = comment['info']['UserName'].lower()
                # 截止时间为2018年12月11日 并且 附上自己的博客才算报名
                if comment['info']['Content'].find('csdn.net/'+username) > -1 and comment['info']['PostTime'] <= '2018-12-12 12:00:00' :
                    # 喜欢重复刷评论的小哥哥,刷了多次也只算一次啊
                    if username not in __class__.user_set:
                        __class__.user_set.add(username)
                        #接下来到这里拉用户信息
                        yield scrapy.Request('https://blog.csdn.net/'+username, callback=lambda response, info=comment['info']: self.parse_blog_user_info(response,info))

    def parse_blog_user_info(self,response,info):
        info['Content'] = info['Content'].replace('\n','')
        item = CSDN2018BlogStarItem()
        item['link'] = response.request.url
        item['blogstar_comment'] = info
        item['blog_title'] = response.xpath('//div[@class="title-box"]/h1[@class="title-blog"]/a/text()').extract_first()
        item['description'] = response.xpath('//div[@class="title-box"]/p[@class="description"]/text()').extract_first()
        item['avatar_pic'] = response.xpath('//div[@class="profile-intro d-flex"]/div[@class="avatar-box d-flex justify-content-center flex-column"]/a/img/@src').extract_first()

        for data in response.xpath('//div[@class="data-info d-flex item-tiling"]/dl[@class="text-center"]'):
            data_key = data.xpath('./dt/a/text() | ./dt/text()').extract_first()
            data_value = data.xpath('./@title').extract_first()
            if data_key.find('原创') > -1:
                item['original'] = int(data_value)
            elif data_key.find('粉丝') > -1:
                item['fans'] = int(data_value)
            elif data_key.find('喜欢') > -1:
                item['star'] = int(data_value)
            elif data_key.find('评论') > -1:
                item['comment'] = int(data_value)
        for grade in response.xpath('//div[@class="grade-box clearfix"]/dl'):
            grade_key = grade.xpath('./dt/text()').extract_first()
            grade_value = grade.xpath('./dd/@title | ./dd/a/@title | ./@title').extract_first()
            if grade_key.find('等级') > -1:
                item['level'] = int(grade_value.replace('级,点击查看等级说明',''))
            elif grade_key.find('访问') > -1:
                item['visit'] = int(grade_value)
            elif grade_key.find('积分') > -1:
                item['score'] = int(grade_value)
            elif grade_key.find('排名') > -1:
                item['rank'] = int(grade_value)

        #勋章
        item['medal'] = response.xpath('//div[@class="badge-box d-flex"]/div[@class="icon-badge"]/@title').extract()

        blog_expert = ''.join(response.xpath('//div[@class="user-info d-flex justify-content-center flex-column"]/p[@class="flag expert"]/text()').extract()).replace('\n','').replace(' ','')
        if blog_expert and '' is not blog_expert :
            item['medal'].append(blog_expert)

        #归档
        archives = []
        for li in response.xpath('//div[@id="asideArchive"]/div[@class="aside-content"]/ul[@class="archive-list"]/li'):
            archives.append({'year_month':li.xpath('./a/text()').extract_first().replace(' ','').replace('\n',''),'article_num':li.xpath('./a/span/text()').extract_first().replace(' ','').replace('篇','')})

        item['archives'] = archives
        yield item



