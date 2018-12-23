# /usr/bin/env python3
# -*- coding:utf-8 -*-

class Var(object):
    var_12306 = {
        "popup_passport_appId":'otn',
        "popup_passport_baseUrl" : 'https://kyfw.12306.cn/passport/',
        "popup_passport_apptk_static" : 'https://kyfw.12306.cn/passport/web/auth/uamtk-static',
        "popup_passport_login" : 'https://kyfw.12306.cn/passport/web/login',
        "popup_passport_captcha" : 'https://kyfw.12306.cn/passport/' + 'captcha/captcha-image64?login_site=E&module=login&rand=sjrand&',
        "popup_passport_captcha_check" : 'https://kyfw.12306.cn/passport/' + 'captcha/captcha-check',
        "popup_passport_uamtk" : 'https://kyfw.12306.cn/passport/' + 'web/auth/uamtk',
        "popup_is_uam_login" : False, # 是否统一认证登录
        "popup_baseUrl" : 'https://kyfw.12306.cn',
        "popup_publicName" : '/otn', # 预发布环境
        "base_uamauthclient_url" : 'https://kyfw.12306.cn/passport/' + '/otn' + '/uamauthclient',
    }

    def __init__(self):
        pass