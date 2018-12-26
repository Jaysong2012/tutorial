#/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from pathlib import Path
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import asyncio

username =u'username'
password =u'password'

from_station = u'SHH'
from_station_text = u'上海'
to_station = u'WCN'
to_station_text = u'武昌'
travel_date = '"2018-12-25"'
passenger_list = ['张三','李四']
priority_train = [
    {'train_no':'Z27','train_seat':['硬卧','硬座']},
]

seat_no = {
    '商务座':1,
    '一等座':2,
    '二等座':3,
    '高级软卧':4,
    '软卧':5,
    '动卧':6,
    '硬卧':7,
    '软座':8,
    '硬座':9,
    '无座':10
}

seat_type_index = {
    '商务座': '9',
    '一等座': 'M',
    '二等座': '0',
    '高级软卧': '4',
    '软卧': '5',
    '动卧': '6',
    '硬卧': '3',
    '软座': '8',
    '硬座': '1',
    '无座': '10'
}

time_out = 60
poll_frequency = 0.1
requery_frequency = 1

requery =True
has_jump_buy_page = False

def has_seat(row_list,no):
    # bus_seat = row_list[1] == '有' or isinstance(row_list[1],int)
    # first_seat = row_list[2] == '有' or isinstance(row_list[2],int)
    # second_seat = row_list[3] == '有' or isinstance(row_list[3],int)
    # high_grade_soft_berth = row_list[4] == '有' or isinstance(row_list[4],int)
    # soft_berth = row_list[5] == '有' or isinstance(row_list[5],int)
    # motor_berth = row_list[6] == '有' or isinstance(row_list[6],int)
    # hard_berth = row_list[7] == '有' or isinstance(row_list[7],int)
    # soft_seat = row_list[8] == '有' or isinstance(row_list[8],int)
    # hard_seat = row_list[9] == '有' or iisinstancent(row_list[9],int)
    # no_seat = row_list[10] == '有' or isinstance(row_list[10],int)
    return row_list[no] == '有' or isinstance(row_list[no],int)

def wait_loading_or_exit(driver,xpath,msg='等待加载完成'):
    try:
        print(msg)
        WebDriverWait(driver, time_out, poll_frequency).until(
            lambda x: x.find_element_by_xpath(xpath).is_displayed())
    except Exception as e:
        if isinstance(e,TimeoutException):
            print('网络超时，即将退出并重试',e)
        else:
            print(e)
        driver.close()
        exit(1)

def query_ticket_success(driver):
    for i in range(60):
        try:
            EC.visibility_of_element_located(driver.find_element_by_xpath('//div[@class="sear-result"]'))
            print('车票信息查询成功')
            return True
        except Exception as e:
            print(e)

        try:
            EC.visibility_of_element_located(driver.find_element_by_xpath('//div[@class="no-ticket"]'))
            print('车票信息查询失败')
            return False
        except Exception as e:
            print(e)
        time.sleep(0.1)
    return False

def query_ticket_click(driver):
    print('点击查询按钮')
    driver.find_element_by_xpath('//a[@id="query_ticket"]').click()
    time.sleep(1)

    print('等待查询按钮恢复可点击状态')
    try:
        WebDriverWait(driver, 60, 0.1).until(
            lambda x: x.find_element_by_xpath('//a[@id="query_ticket"]').is_enabled())
    except Exception as e:
        if isinstance(e, TimeoutException):
            print('网络超时，即将退出并重试', e)
        else:
            print(e)
        driver.close()
        exit(1)

    time.sleep(1)

@asyncio.coroutine
def async_tr(tr):
    # 将每一个tr的数据根据td查询出来，返回结果为list对象
    row_list = [td.text for td in tr.find_elements_by_xpath('./td')]
    print(row_list)
    if len(row_list) > 0:
        train_no = row_list[0].split('\n')[0]
        for priority in priority_train:
            if train_no == priority['train_no']:
                for seat in priority['train_seat']:
                    if has_seat(row_list, seat_no[seat]):
                        requery = False
                        tr.find_element_by_xpath('./td/a').click()
                        print("跳转到购买页")
                        break

async def async_tr_s(tr):
    return tr.find_elements_by_xpath('./td')

@asyncio.coroutine
def async_tr_row_list(tr):
    global requery,has_jump_buy_page
    try:
        # 将每一个tr的数据根据td查询出来，返回结果为list对象
        eles = yield from async_tr_s(tr)
        if eles:
            row_list = [td.text for td in eles]
            print(row_list)
            if len(row_list) > 0:
                train_no = row_list[0].split('\n')[0]
                for priority in priority_train:
                    if train_no == priority['train_no']:
                        for seat in priority['train_seat']:
                            if has_seat(row_list, seat_no[seat]):
                                requery = False

                                tr.find_element_by_xpath('./td/a').click()
                                print("跳转到购买页")
                                has_jump_buy_page = True
                                break
    except Exception as e:
        print(e)
        if has_jump_buy_page:
            print('已经跳转到购买页，所以查找失败，暂无影响')


async def async_tr_row_list_await(tr):
    global requery,has_jump_buy_page
    try:
        # 将每一个tr的数据根据td查询出来，返回结果为list对象
        eles = await async_tr_s(tr)
        if eles:
            row_list = [td.text for td in eles]
            print(row_list)
            if len(row_list) > 0:
                train_no = row_list[0].split('\n')[0]
                for priority in priority_train:
                    if train_no == priority['train_no']:
                        for seat in priority['train_seat']:
                            if has_seat(row_list, seat_no[seat]):
                                requery = False

                                tr.find_element_by_xpath('./td/a').click()
                                print("跳转到购买页")
                                has_jump_buy_page = True
                                break
    except Exception as e:
        print(e)
        if has_jump_buy_page:
            print('已经跳转到购买页，所以查找失败，暂无影响')

def loop_await(tasks):
    global requery, has_jump_buy_page
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
    except Exception as e:
        print(e)
        if has_jump_buy_page:
            print('已经跳转到购买页，查找失败')
    finally:
        if loop:
            loop.close()

def buy_ticket_or_requery(driver):
    global requery, has_jump_buy_page
    query_ticket_click(driver)

    while not query_ticket_success(driver):
        query_ticket_click(driver)

    #requery = True
    # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
    #for i,tr in enumerate(driver.find_elements_by_xpath('//tbody[@id="queryLeftTable"]/tr')):  # 遍历每一个tr
    loop_await([async_tr_row_list_await(tr) for tr in driver.find_elements_by_xpath('//tbody[@id="queryLeftTable"]/tr')])


    print(requery,has_jump_buy_page)
    # try:
    #     time.sleep(10)
    # except Exception as e:
    #     print(e)
    #
    if requery:
        print('没有票，将再次发起查询')
        buy_ticket_or_requery(driver)

def get_right_train(buy_train_no):
    for priority in priority_train:
        if priority['train_no'] == buy_train_no :
            return priority

if __name__ == '__main__':
    # 加载webdriver驱动，用于获取登录页面标签属性
    driver = webdriver.Chrome('/data/code/python/venv/venv_Scrapy/tutorial/chromedriver')
    # 加载页面
    driver.get('https://kyfw.12306.cn/otn/resources/login.html')

    wait_loading_or_exit(driver,'//div[@class="login-code"]/div[@class="login-code-con"]/div[@class="login-code-main"]/div[@class="code-pic"]/img[@id="J-qrImg"]','等待扫码登录登录码加载完成')

    #模拟执行js代码，隐藏扫码登录
    # js = "var ele = document.getElementsByClassName(\"login-code\")[0];ele.style.display=\"none\";"  # 编写JS语句
    # driver.execute_script(js)  # 执行JS

    driver.find_element_by_xpath(
        '//div[@class="login-box"]/ul[@class="login-hd"]/li[@class="login-hd-account"]/a').click()

    driver.find_element_by_xpath('//input[@id="J-userName"]').clear()
    driver.find_element_by_xpath('//input[@id="J-userName"]').send_keys(username)  # 填充用户名

    driver.find_element_by_xpath('//input[@id="J-password"]').clear()
    driver.find_element_by_xpath('//input[@id="J-password"]').send_keys()  # 填充用户名

    wait_loading_or_exit(driver,'//div[@class="touclick-wrapper lgcode-2018"]/div[@id="J-loginImgArea"]/img[@id="J-loginImg"]','等待图形验证码加载完成')


    input_no = input("请检查网页是否有图形验证码需要点击，需要的化就请在在网页点击验证码图片，点击完成后，控制台输入1回车；如果无需点击验证码，则直接回车")
    if input_no and '' != input_no and int(input_no) == 1:
        driver.find_element_by_xpath('//div[@class="login-btn"]/a[@class="btn btn-primary form-block"]').click()

    #wait_loading_or_exit(driver,'//div[@class="login-account"]/div[@class="login-pwd-code"]/div[@class="touclick-wrapper lgcode-2018"]/div[@class="lgcode-success"]','等待图形验证码验证完成')

    wait_loading_or_exit(driver,'//li[@id="J-header-logout"]','等待登录完成')

    wait_loading_or_exit(driver, '//li[@id="J-chepiao"]/a', '等待车票按钮显示完成')

    print('鼠标放到车票按钮上')
    ActionChains(driver).move_to_element(driver.find_element_by_xpath('//li[@id="J-chepiao"]/a')).perform()

    wait_loading_or_exit(driver, '//div[@class="nav-bd-item nav-col2"]/ul[@class="nav-con"]/li[@class="nav_dan"]/a', '等待单程按钮显示完成')

    print('点击单程按钮，加载查询车票页')
    driver.find_element_by_xpath('//div[@class="nav-bd-item nav-col2"]/ul[@class="nav-con"]/li[@class="nav_dan"]/a').click()

    wait_loading_or_exit(driver, '//input[@id="fromStationText"]', '等待查询车票页面加载完成')

    print('填充购票车站信息')
    fromStation = driver.find_element_by_xpath('//input[@id="fromStation"]')
    driver.execute_script('arguments[0].removeAttribute(\"type\")', fromStation)

    driver.find_element_by_xpath('//input[@id="fromStationText"]').clear()
    driver.find_element_by_xpath('//input[@id="fromStationText"]').send_keys(from_station_text)  # 填充出发点

    driver.find_element_by_xpath('//input[@id="fromStation"]').clear()
    driver.find_element_by_xpath('//input[@id="fromStation"]').send_keys(from_station)  # 填充出发点

    toStation = driver.find_element_by_xpath('//input[@id="toStation"]')
    driver.execute_script('arguments[0].removeAttribute(\"type\")', toStation)

    driver.find_element_by_xpath('//input[@id="toStationText"]').clear()
    driver.find_element_by_xpath('//input[@id="toStationText"]').send_keys(to_station_text)  # 填充目的地

    driver.find_element_by_xpath('//input[@id="toStation"]').clear()
    driver.find_element_by_xpath('//input[@id="toStation"]').send_keys(to_station)  # 填充目的地

    js = 'document.getElementById("train_date").removeAttribute("readonly");'
    driver.execute_script(js)
    # 清空文本框再输入值
    # driver.find_element_by_id("train_date").clear()
    # driver.find_element_by_id("train_date").send_keys("2018-7-25")
    # JS直接输入
    js_value = 'document.getElementById("train_date").value='+travel_date
    driver.execute_script(js_value)
    # driver.find_element_by_xpath('//input[@class="inp_selected"]').clear()
    # driver.find_element_by_xpath('//input[@class="inp_selected"]').send_keys(u'')  # 填充出发时间

    #query_ticket_click(driver)

    # try:
    #     WebDriverWait(driver, 3, 0.1).until(
    #         lambda x: x.find_element_by_xpath('//div[@class="sear-result"]').is_displayed())
    # except Exception as e:
    #     if isinstance(e,TimeoutException):
    #         print('网络超时，即将退出并重试',e)
    #         try:
    #             EC.visibility_of_element_located(driver.find_element_by_xpath('//div[@class="no-ticket"]'))
    #             print('查询失败，需要重复点击查询', e)
    #             driver.find_element_by_xpath('//a[@id="query_ticket"]').click()
    #             time.sleep(5)
    #         except Exception as e:
    #             print(e)
    #     else:
    #         print(e)
    #         driver.close()
    #         exit(1)

    buy_ticket_or_requery(driver)

    wait_loading_or_exit(driver, '//ul[@id="normal_passenger_id"]', '等待乘车人列表加载完成')

    normal_passenger_li_list = driver.find_elements_by_xpath('//ul[@id="normal_passenger_id"]/li')

    for li in normal_passenger_li_list:
        name_label = li.find_element_by_xpath('./label').text
        for passenger in passenger_list:
            if name_label.find(passenger) > -1:
                print('选择乘车人')
                li.find_element_by_xpath('./input').click()

    buy_train_no = driver.find_element_by_xpath('//p[@id="ticket_tit_id"]/strong[@class="ml5"]').text

    # 实例化一个Select类的对象
    print('选择座位类型')
    selector = Select(driver.find_element_by_id("seatType_1"))
    right_train = get_right_train(buy_train_no)
    print(buy_train_no,right_train)
    for train_seat in right_train['train_seat']:
        if seat_type_index[train_seat] in selector.options:
            selector.select_by_value(seat_type_index[train_seat])  # 通过index进行选择,index从0开始


    print('点击提交购票按钮')
    driver.find_element_by_id("submitOrder_id").click()

    print('等待确认购买按钮加载完成')
    try:
        WebDriverWait(driver, 10, 0.1).until(
            lambda x: x.find_element_by_id("qr_submit_id").is_displayed())
    except Exception as e:
        if isinstance(e,TimeoutException):
            print('网络超时，即将退出并重试',e)
        else:
            print(e)
        driver.close()
        exit(1)

    print('点击确认购买按钮')
    # driver.find_element_by_id("qr_submit_id").click()

    input("这里按下确认，完成购买")

    driver.close()
    exit(1)