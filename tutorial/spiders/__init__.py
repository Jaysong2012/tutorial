# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from aip import AipImageClassify

""" 你的 APPID AK SK """
APP_ID = '15229602'
API_KEY = '2lLuZ6I7n7rwI5nx3AE0Nkdo'
SECRET_KEY = 'MN6LFbV0DTizVS0zdvCcMgZqTYB1YGBF'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
