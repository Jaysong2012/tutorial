#! /usr/bin/env
# -*- coding:utf-8 -*-

import requests
import json
import time
import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import os
import re

code_login = True
time_out = 60
poll_frequency = 0.1
requery = True

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

def print_t(*content):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),*content)

def get_citylist_from_12306():
    dict_city = {}
    s_list = re.findall('var station_names =\'(.*?)\';', requests.get('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js').text)[0].split('@')
    for s in s_list:
        if '' == s:
            continue
        l_list = s.split('|')
        dict_city[l_list[1]] = l_list[2]

    return dict_city

# 下载所有的车次数据  保存为 train_list.txt文件
def get_train_list():
    requests.adapters.DEFAULT_RETRIES = 5
    response = requests.get('https://kyfw.12306.cn/otn/resources/js/query/train_list.js', stream=True, verify=False)
    status = response.status_code
    if status == 200:
        with open('./config/train_list.txt', 'wb') as of:
            for chunk in response.iter_content(chunk_size=102400):
                if chunk:
                    of.write(chunk)

def get_train_no(train_code,train_date):
    c = list(train_code)[0]
    with open('./config/train_list.txt', 'rb') as of:
        text = of.readline()
        tt = text.decode("utf-8")
        ss = tt.replace('var train_list =','').replace("},{", "},\n{")

        d = json.loads(ss)

        for k in d[train_date][c]:
            if k['station_train_code'].find(train_code+'(')>-1:
                return k['train_no']

def wait_loading_or_exit(driver,xpath,msg='等待加载完成'):
    try:
        print_t(msg)
        WebDriverWait(driver, time_out, poll_frequency).until(
            lambda x: x.find_element_by_xpath(xpath).is_displayed())
    except Exception as e:
        if isinstance(e,TimeoutException):
            print_t('网络超时，即将退出,请确认网络后发起重试')
        else:
            print_t(e)
        driver.close()
        exit(1)

def click_query_ticket(driver):
    try:
        driver.find_element_by_xpath('//a[@id="query_ticket"]').click()
    except Exception as e:
        if not check_query_ticket_success(driver):
            time.sleep(1)
            click_query_ticket(driver)


    print_t('点击查询按钮并且等待恢复可点击状态(等待查询完成)')
    try:
        WebDriverWait(driver, 60, 0.1).until(
            lambda x: x.find_element_by_xpath('//a[@id="query_ticket"]').is_enabled())
    except Exception as e:
        if isinstance(e, TimeoutException):
            print_t('网络超时，即将退出,请确认网络后发起重试')
        else:
            print(e)
        driver.close()
        exit(1)

    time.sleep(1)

def check_query_ticket_success(driver):
    try:
        EC.visibility_of_element_located(driver.find_element_by_xpath('//div[@class="sear-result"]'))
        print_t('车票信息查询成功')
        return True
    except Exception as e:
        print(e)

    try:
        EC.visibility_of_element_located(driver.find_element_by_xpath('//div[@class="no-ticket"]'))
        print_t('车票信息查询失败')
        return False
    except Exception as e:
        print(e)
    return False

def query_ticket_or_requery(driver):
    global requery
    click_query_ticket(driver)

    while not check_query_ticket_success(driver):
        click_query_ticket(driver)

    try:
        tr = driver.find_element_by_id("ticket_"+train_no)
        row_list =[td.text for td in tr.find_elements_by_xpath('./td')]
        print_t(row_list)
        if len(row_list) > 0:
            train_code = row_list[0].split('\n')[0]
            print_t(train_code)
            if train_code == ticket_12306_config_dict['train_code']:
                for seat in ticket_12306_config_dict['train_seat']:
                    print_t(seat)
                    if has_seat(row_list, seat_no[seat]):
                        requery = False

                        tr.find_element_by_xpath('./td/a').click()
                        print_t("查票成功跳转到购买页")
                        break
    except Exception as e:
        if isinstance(e,NoSuchElementException):
            print_t("没有找到该车次，可能该车次已经停售，系统将继续尝试，你可以Ctrl C退出选择其他车次")

    if requery:
        print_t('没有票，将再次发起查询')
        query_ticket_or_requery(driver)

def has_seat(row_list,no):
    return row_list[no] == '有' or isinstance(int(row_list[no]),int)


def get_right_train(buy_train_code,ticket_12306_config_dict):
    for priority in ticket_12306_config_dict['priority_train']:
        if priority['train_code'] == buy_train_code :
            return priority

if __name__ == '__main__':
    print_t('开始读取配置文件')
    try:
        with open('./config/ticket_12306_exact_mode_config.json','r') as f:
            ticket_12306_config = f.read()
    except FileNotFoundError as e:
        print_t('没有找到配置文件，系统已退出，请先下载配置文件ticket_12306_config.json到当前运行环境目录下的config目录')
        exit(1)

    ticket_12306_config_dict = json.loads(ticket_12306_config)
    print_t('配置文件读取成功')

    print_t('开始加载全部城市列表')
    try:
        with open('./config/ticket_12306_citylist.json','r') as f:
            ticket_12306_citylist = f.read()
            ticket_12306_citylist_dict = json.loads(ticket_12306_citylist)
    except FileNotFoundError as e:
        print_t('没有找到全部城市列表文件，系统将从网络下载，为提高速度请先下载全部城市列表ticket_12306_citylist.json到当前运行环境目录下的config目录')
        try:
            ticket_12306_citylist_dict = get_citylist_from_12306()
        except Exception as e2:
            print_t('系统从网络下载全部城市列表失败，系统将退出')
            exit(1)

    print_t('全部城市列表读取成功')

    if ticket_12306_citylist_dict.get(ticket_12306_config_dict['from_station_text'],'') == ''\
            or ticket_12306_citylist_dict.get(ticket_12306_config_dict['to_station_text'],'') == '':
        print_t('请填写正确的车次信息')
        exit(1)

    ticket_12306_config_dict['from_station'] = ticket_12306_citylist_dict[ticket_12306_config_dict['from_station_text']]
    ticket_12306_config_dict['to_station'] = ticket_12306_citylist_dict[ticket_12306_config_dict['to_station_text']]

    try:
        datetime.datetime.strptime(re.findall('\'(.*?)\'', ticket_12306_config_dict['travel_date'])[0], '%Y-%m-%d')
    except ValueError as e:
        print_t('请填写正确的出发时间信息')
        exit(1)

    if not os.path.exists("./config/train_list.txt"):
        print_t('开始下载当前12306全部车次信息，50M左右，下载时间比较长，请耐心等待')
        get_train_list()
        print_t('下载当前12306全部车次信息，50M左右，下载完成')

    train_no = get_train_no(ticket_12306_config_dict['train_code'],ticket_12306_config_dict['travel_date'].replace('\'',''))
    if not train_no:
        print_t('你当前要购买的车次不存在，无法购买，系统将退出')


    print_t('系统配置读取完成')
    print('   您将为',ticket_12306_config_dict['passenger_list'],'购买在',\
            ticket_12306_config_dict['travel_date'],'由',ticket_12306_config_dict['from_station_text'],\
            '开往', ticket_12306_config_dict['to_station_text'],'的列车')
    print('   系统将选择',ticket_12306_config_dict['train_code'],'列车的',ticket_12306_config_dict['train_seat'],'席位')


    print_t('准备完成即将开始购票')

    driver = webdriver.Chrome('./chromedriver')

    print_t('开始进入登录页面')
    driver.get('https://kyfw.12306.cn/otn/resources/login.html')

    wait_loading_or_exit(driver,'//div[@class="login-code"]/div[@class="login-code-con"]/div[@class="login-code-main"]/div[@class="code-pic"]/img[@id="J-qrImg"]','等待扫码登录登录码加载完成')

    print_t('系统目前启用扫码登录，请打开手机12306客户端完成扫码登录，启用账户密码的方式为修改为 code_login 为 False')
    if not code_login:
        driver.find_element_by_xpath(
            '//div[@class="login-box"]/ul[@class="login-hd"]/li[@class="login-hd-account"]/a').click()

        print_t('开始自动填充用户名密码')

        driver.find_element_by_xpath('//input[@id="J-userName"]').clear()
        driver.find_element_by_xpath('//input[@id="J-userName"]').send_keys(ticket_12306_config_dict['username'])  # 填充用户名

        driver.find_element_by_xpath('//input[@id="J-password"]').clear()
        driver.find_element_by_xpath('//input[@id="J-password"]').send_keys(ticket_12306_config_dict['password'])  # 填充用户名

        wait_loading_or_exit(driver,
                             '//div[@class="touclick-wrapper lgcode-2018"]/div[@id="J-loginImgArea"]/img[@id="J-loginImg"]',
                             '等待图形验证码加载完成')

    input_no = input("请检查网页是否有图形验证码需要点击，需要就请在在网页点击验证码图片，点击完成后，控制台输入1回车；如果无需点击验证码，则直接回车")
    if input_no and '' != input_no and int(input_no) == 1:
        driver.find_element_by_xpath('//div[@class="login-btn"]/a[@class="btn btn-primary form-block"]').click()


    wait_loading_or_exit(driver, '//li[@id="J-header-logout"]', '等待登录完成')

    wait_loading_or_exit(driver, '//li[@id="J-chepiao"]/a', '等待车票按钮显示完成')

    print_t('自动将鼠标放到车票按钮上')
    ActionChains(driver).move_to_element(driver.find_element_by_xpath('//li[@id="J-chepiao"]/a')).perform()

    wait_loading_or_exit(driver, '//div[@class="nav-bd-item nav-col2"]/ul[@class="nav-con"]/li[@class="nav_dan"]/a', '等待单程按钮显示完成')

    print_t('自动点击单程按钮，加载查询车票页')
    driver.find_element_by_xpath('//div[@class="nav-bd-item nav-col2"]/ul[@class="nav-con"]/li[@class="nav_dan"]/a').click()

    wait_loading_or_exit(driver, '//input[@id="fromStationText"]', '等待查询车票页面加载完成')

    print_t('自动填充购票车站信息')
    fromStation = driver.find_element_by_xpath('//input[@id="fromStation"]')
    driver.execute_script('arguments[0].removeAttribute(\"type\")', fromStation)

    driver.find_element_by_xpath('//input[@id="fromStationText"]').clear()
    driver.find_element_by_xpath('//input[@id="fromStationText"]').send_keys(ticket_12306_config_dict['from_station_text'])

    driver.find_element_by_xpath('//input[@id="fromStation"]').clear()
    driver.find_element_by_xpath('//input[@id="fromStation"]').send_keys(ticket_12306_config_dict['from_station'])

    toStation = driver.find_element_by_xpath('//input[@id="toStation"]')
    driver.execute_script('arguments[0].removeAttribute(\"type\")', toStation)

    driver.find_element_by_xpath('//input[@id="toStationText"]').clear()
    driver.find_element_by_xpath('//input[@id="toStationText"]').send_keys(ticket_12306_config_dict['to_station_text'])  # 填充目的地

    driver.find_element_by_xpath('//input[@id="toStation"]').clear()
    driver.find_element_by_xpath('//input[@id="toStation"]').send_keys(ticket_12306_config_dict['to_station'])  # 填充目的地

    js = 'document.getElementById("train_date").removeAttribute("readonly");'
    driver.execute_script(js)
    js_value = 'document.getElementById("train_date").value='+ticket_12306_config_dict['travel_date']
    driver.execute_script(js_value)

    print_t('将开始发起查询')
    query_ticket_or_requery(driver)

    wait_loading_or_exit(driver, '//ul[@id="normal_passenger_id"]', '等待乘车人列表加载完成')

    normal_passenger_li_list = driver.find_elements_by_xpath('//ul[@id="normal_passenger_id"]/li')

    for li in normal_passenger_li_list:
        name_label = li.find_element_by_xpath('./label').text
        for passenger in ticket_12306_config_dict['passenger_list']:
            if name_label.find(passenger) > -1:
                print_t('自动选择乘车人',passenger)
                li.find_element_by_xpath('./input').click()

    buy_train_code = driver.find_element_by_xpath('//p[@id="ticket_tit_id"]/strong[@class="ml5"]').text

    for i,passerger in enumerate(ticket_12306_config_dict['passenger_list']):
        selector = Select(driver.find_element_by_id("seatType_"+str(i+1)))
        select_seat_list = [o.text.replace(' ','').replace('\n','')  for o in selector.options]
        print_t('自动选择座位类型，目前可选择的座位类型有',select_seat_list)

        set_seat_success = False
        for train_seat in ticket_12306_config_dict['train_seat']:
            for i,select_seat in enumerate(select_seat_list):
                if select_seat.find(train_seat)>-1 and not set_seat_success:
                    print_t('为',passerger,'自动选择座位类型，目前为你成功选择座位类型为', train_seat)
                    selector.select_by_index(i)
                    set_seat_success = True
                    break


    print_t('自动点击提交购票按钮')
    driver.find_element_by_id("submitOrder_id").click()

    print_t('等待确认购买按钮加载完成')
    try:
        WebDriverWait(driver, 10, 0.1).until(
            lambda x: x.find_element_by_id("qr_submit_id").is_displayed())
    except Exception as e:
        if isinstance(e,TimeoutException):
            print_t('网络超时，即将退出,请确认网络后发起重试')
        else:
            print(e)
        driver.close()
        exit(1)

    print_t('自动点击确认购买按钮')
    driver.find_element_by_id("qr_submit_id").click()

    input("完成购买！请在30分钟内登录账户，完成付款,点击Enter退出购票")

    driver.close()
    exit(1)