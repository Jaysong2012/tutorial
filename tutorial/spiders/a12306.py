# -*- coding: utf-8 -*-
import scrapy
from backend.libs.Var import Var
import time
import json
from PIL import Image
import base64
import io
from . import client
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path
from selenium.webdriver.support.select import Select


class A12306Spider(scrapy.Spider):
    name = '12306'
    allowed_domains = ['kyfw.12306.cn']
    start_urls = ['https://kyfw.12306.cn/otn/resources/login.html','https://kyfw.12306.cn/otn/leftTicket/init']

    def start_requests(self):
        # 加载webdriver驱动，用于获取登录页面标签属性
        driver = webdriver.Chrome('/data/code/python/venv/venv_Scrapy/tutorial/chromedriver')
        #加载页面
        driver.get(self.start_urls[0])

        WebDriverWait(driver, 8, 0.5, ignored_exceptions=TimeoutException).until(
            lambda x: x.find_element_by_xpath('//div[@class="login-code"]').is_displayed())

        input("Enter 2 Exit")
        time.sleep(1)

        js = "var ele = document.getElementsByClassName(\"login-code\")[0];ele.style.display=\"none\";"  # 编写JS语句
        driver.execute_script(js)  # 执行JS

        driver.find_element_by_xpath('//div[@class="login-box"]/ul[@class="login-hd"]/li[@class="login-hd-account"]/a').click()
        driver.find_element_by_xpath('//input[@id="J-userName"]').clear()
        driver.find_element_by_xpath('//input[@id="J-userName"]').send_keys(u'jaysong2012')  # 填充用户名

        driver.find_element_by_xpath('//input[@id="J-password"]').clear()
        driver.find_element_by_xpath('//input[@id="J-password"]').send_keys(u'java11250626')  # 填充用户名

        input_no = input("检查网页是否有验证码要输入，有就在网页输入验证码，输入完后，控制台输入1回车；如果无验证码，则直接回车")
        if input_no and '' != input_no and int(input_no) == 1:
            driver.find_element_by_xpath('//div[@class="login-btn"]/a[@class="btn btn-primary form-block"]').click()

        input("检查网页是否有完成登录跳转，如果完成则直接回车")



        WebDriverWait(driver, 10, 0.5, ignored_exceptions=TimeoutException).until(
            lambda x: x.find_element_by_xpath('//li[@id="J-header-logout"]').is_displayed())
        #加载页面
        driver.get(self.start_urls[1])

        input("Enter 2 Exit")

        fromStation = driver.find_element_by_xpath('//input[@id="fromStation"]')
        driver.execute_script('arguments[0].removeAttribute(\"type\")', fromStation)

        driver.find_element_by_xpath('//input[@id="fromStationText"]').clear()
        driver.find_element_by_xpath('//input[@id="fromStationText"]').send_keys(u'上海')  # 填充出发点

        driver.find_element_by_xpath('//input[@id="fromStation"]').clear()
        driver.find_element_by_xpath('//input[@id="fromStation"]').send_keys(u'SHH')  # 填充出发点

        toStation = driver.find_element_by_xpath('//input[@id="toStation"]')
        driver.execute_script('arguments[0].removeAttribute(\"type\")', toStation)

        driver.find_element_by_xpath('//input[@id="toStationText"]').clear()
        driver.find_element_by_xpath('//input[@id="toStationText"]').send_keys(u'襄阳')  # 填充目的地

        driver.find_element_by_xpath('//input[@id="toStation"]').clear()
        driver.find_element_by_xpath('//input[@id="toStation"]').send_keys(u'XFN')  # 填充目的地

        js = 'document.getElementById("train_date").removeAttribute("readonly");'
        driver.execute_script(js)
        # 清空文本框再输入值
        # driver.find_element_by_id("train_date").clear()
        # driver.find_element_by_id("train_date").send_keys("2018-7-25")
        # JS直接输入
        js_value = 'document.getElementById("train_date").value="2018-12-25"'
        driver.execute_script(js_value)
        #driver.find_element_by_xpath('//input[@class="inp_selected"]').clear()
        #driver.find_element_by_xpath('//input[@class="inp_selected"]').send_keys(u'')  # 填充出发时间

        time.sleep(1)

        driver.find_element_by_xpath('//a[@id="query_ticket"]').click()


        WebDriverWait(driver, 10, 0.5, ignored_exceptions=TimeoutException).until(
            lambda x: x.find_element_by_xpath('//div[@class="sear-result"]').is_displayed())

        time.sleep(1)

        input("Enter 2 Exit")

        # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
        table_tr_list = driver.find_element_by_xpath('//div[@class="t-list"]/table/tbody[@id="queryLeftTable"]').find_elements_by_xpath('./tr')

        for tr in table_tr_list:  # 遍历每一个tr
            # 将每一个tr的数据根据td查询出来，返回结果为list对象
            row_list = [td.text for td in tr.find_elements_by_xpath('./td')]
            print(row_list)
            if len(row_list)>0 and row_list[0].find('K282')>-1 and row_list[-1] =='预订':
                tr.find_element_by_xpath('./td/a').click()
                input("跳转到购买页")
                break;


        WebDriverWait(driver, 10, 0.5, ignored_exceptions=TimeoutException).until(
            lambda x: x.find_element_by_xpath('//ul[@id="normal_passenger_id"]').is_displayed())

        input("Enter 2 Exit")

        normal_passenger_li_list = driver.find_elements_by_xpath('//ul[@id="normal_passenger_id"]/li')

        for li in normal_passenger_li_list:
            if li.find_element_by_xpath('./label').text.find('宋超')>-1:
                li.find_element_by_xpath('./input').click()

        # 实例化一个Select类的对象
        selector = Select(driver.find_element_by_id("seatType_1"))

        # 下面三种方法用于选择"篮球运动员"
        selector.select_by_value("3")  # 通过index进行选择,index从0开始


        driver.find_element_by_id("submitOrder_id").click()

        input("Enter 2 Exit")

        WebDriverWait(driver, 10, 0.5, ignored_exceptions=TimeoutException).until(
            lambda x: x.find_element_by_id("qr_submit_id").is_displayed())

        time.sleep(1)

        #driver.find_element_by_id("qr_submit_id").click()

        input("这里按下确认，完成购买")

    def query_ticket(self):
        if not Path('12306Cookies.json').exists():
            __class__.login()  # 先执行login，保存cookies之后便可以免登录操作

        # 毕竟每次执行都要登录还是挺麻烦的，我们要充分利用cookies的作用
        # 从文件中获取保存的cookies
        with open('12306Cookies.json', 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())  # 获取cookies

        # 把获取的cookies处理成dict类型
        cookies_dict = dict()
        for cookie in listcookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_dict[cookie['name']] = cookie['value']

        # Scrapy发起其他页面请求时，带上cookies=cookies_dict即可，同时记得带上header值，
        yield scrapy.Request(url='https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-12-21&leftTicketDTO.from_station=SHH&leftTicketDTO.to_station=NCG&purpose_codes=ADULT', cookies=cookies_dict, callback=self.parse_query, headers=__class__.get_request_header())


    def submit_order(self):
        if not Path('12306Cookies.json').exists():
            __class__.login()  # 先执行login，保存cookies之后便可以免登录操作

        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {
            'secretStr':'ObCp6qlXEjCeLYvfM5bYaGwMNiYb7Ny7Tc99NasIB7vLFRgGG9E2MxxSb7WgCdMk2AwMo%2Fv%2FrLIf%0A74OJLBcggzrdvb1hfuTWkcLh55qJ1Fa7AAXuEhZgP8cZaIiKLKZ6RMQ0EhK1hxhizlfkn4D%2BCZQ7%0AmCEmlgSLPawRTtfJ4mGctkOlYb%2Fjpe%2FDidRhlau95IDEUejWyOWpfupevxWji%2FI0J5QI5IM9POt%2B%0AJzcCL%2FOKUshyBNGUPJvs0B3VntXsoUAeJ1RXzFY%3D',
            'train_date':'2018-12-21' ,
            'back_train_date':'2018-12-21',
            'tour_flag':'dc',
            'purpose_codes':'ADULT',
            'query_from_station_name':'上海',
            'query_to_station_name':'南昌'
        }

        # 毕竟每次执行都要登录还是挺麻烦的，我们要充分利用cookies的作用
        # 从文件中获取保存的cookies
        with open('12306Cookies.json', 'r', encoding='utf-8') as f:
            listcookies = json.loads(f.read())  # 获取cookies

        # 把获取的cookies处理成dict类型
        cookies_dict = dict()
        for cookie in listcookies:
            # 在保存成dict时，我们其实只要cookies中的name和value，而domain等其他都可以不要
            cookies_dict[cookie['name']] = cookie['value']

        # Scrapy发起其他页面请求时，带上cookies=cookies_dict即可，同时记得带上header值，
        yield scrapy.FormRequest(url, cookies=cookies_dict, callback=self.parse_submit, headers=__class__.get_request_header(),formdata=data,method='POST')

    @classmethod
    def login(cls):
        # 加载webdriver驱动，用于获取登录页面标签属性
        driver = webdriver.Chrome('/data/code/python/venv/venv_Scrapy/tutorial/chromedriver')
        #加载页面
        driver.get(cls.start_urls[0])



        time.sleep(3)  # 执行休眠3s等待浏览器的加载

        driver.find_element_by_xpath('//div[@class="login-box"]/ul[@class="login-hd"]/li[@class="login-hd-account"]/a').click()
        driver.find_element_by_xpath('//input[@id="J-userName"]').clear()
        driver.find_element_by_xpath('//input[@id="J-userName"]').send_keys(u'jaysong2012')  # 填充用户名

        driver.find_element_by_xpath('//input[@id="J-password"]').clear()
        driver.find_element_by_xpath('//input[@id="J-password"]').send_keys(u'java11250626')  # 填充用户名

        input_no = input("检查网页是否有验证码要输入，有就在网页输入验证码，输入完后，控制台输入1回车；如果无验证码，则直接回车")
        if int(input_no) == 1:
            driver.find_element_by_xpath('//div[@class="login-btn"]/a[@class="btn btn-primary form-block"]').click()

        input("检查网页是否有完成登录跳转，如果完成则直接回车")

        # 通过上述的方式实现登录后，其实我们的cookies在浏览器中已经有了，我们要做的就是获取
        cookies = driver.get_cookies()  # Selenium为我们提供了get_cookies来获取登录cookies
        driver.close()  # 获取cookies便可以关闭浏览器
        # 然后的关键就是保存cookies，之后请求从文件中读取cookies就可以省去每次都要登录一次的
        # 当然可以把cookies返回回去，但是之后的每次请求都要先执行一次login没有发挥cookies的作用
        jsonCookies = json.dumps(cookies)  # 通过json将cookies写入文件
        with open('12306Cookies.json', 'w') as f:
            f.write(jsonCookies)
        print(cookies)


    def parse_query(self, response):
        dict_rsp = json.loads(response.text)
        result_list = dict_rsp['data']['result']
        print('车次','商务座','一等座','二等座','硬座','硬卧','无座','软卧',)
        for result in result_list:
            result_split_list = result.split('|')
            #print(['_'+(str(i)+'_'+result_split_list_result) for i,result_split_list_result in enumerate(result_split_list)])
            print('|',result_split_list[3],'|',result_split_list[32],'|',result_split_list[31],'|',result_split_list[30],
                  '|',result_split_list[29],'|',result_split_list[28],'|',result_split_list[26],'|',result_split_list[23])
        pass

    def parse_submit(self,response):
        print("*" * 40)
        print("response text: %s" % response.text)
        print("response headers: %s" % response.headers)
        print("response meta: %s" % response.meta)
        print("request headers: %s" % response.request.headers)
        print("request cookies: %s" % response.request.cookies)
        print("request meta: %s" % response.request.meta)

    #        yield scrapy.Request(Var.var_12306['popup_passport_captcha']+str(int(round(time.time()*1000))), headers= __class__.get_request_header(),callback=self.parse)
    def parse_yzm(self, response):
        print("response headers: %s" % response.headers)
        rsp_content_type = response.headers['Content-Type']
        print(rsp_content_type)
        if str(rsp_content_type).find('application/xhtml+xml')>-1:
            return
        elif str(rsp_content_type).find('application/json')>-1:
            print(response.text)
            dict_rep = json.loads(response.text)
            image = dict_rep['image']

            imagedata = base64.b64decode(image)
            with open("./tmp.jpg", 'wb') as fp:
                fp.write(imagedata)

            #image_byte = io.BytesIO(base64.b64decode(image))
            #img = Image.open(base64.b64decode(image))

            """ 如果有可选参数 """
            options = {}
            options["baike_num"] = 10

            """ 带参数调用通用物体识别 """
            client_rsp = client.advancedGeneral(__class__.get_file_content("./tmp.jpg"), options)

            print(json.dumps(client_rsp))
            print(client_rsp)


    @classmethod
    def get_request_header(cls):
        return {
            'Accept': 'application/json;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With':'XMLHttpRequest',
            'Referer':'https://kyfw.12306.cn/otn/resources/login.html',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'kyfw.12306.cn',
            'Pragma':'o-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
        }

    @classmethod
    def get_sub_img(cls,im, x, y):
        assert 0 <= x <= 3
        assert 0 <= y <= 2
        WITH = HEIGHT = 68
        left = 5 + (67 + 5) * x
        top = 41 + (67 + 5) * y
        right = left + 67
        bottom = top + 67

        return im.crop((left, top, right, bottom))

    """ 读取图片 """
    @classmethod
    def get_file_content(cls,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
