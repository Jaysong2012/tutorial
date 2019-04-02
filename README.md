# scrapy实战项目

[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)   [![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)

## tutorial项目结构
```
tutorial/
├── backend                                  #后端辅助demo模块
│   ├── __init__.py 
│   └── libs                                 #自写代码工具类模块
│   └── models                               #数据库模型模块 
│   └── scripts                              #其他单独脚本模块
├── config                                   #参数配置（购票信息这里配置）
│   ├── ticket_12306_citylist.json           #12306全部城市映射
│   ├── ticket_12306_config.json             #扫描模式刷票配置文件
│   ├── ticket_12306_exact_mode_config.json  #精确模式刷票配置文件
├── tutorial
│   ├── __init__.py
│   ├── items.py                             #爬取数据模型
│   ├── middlewares.py                       #中间件案例，详细演示了动态headers动态代理实现
│   ├── pipelines.py                         #爬取数据模型处理
│   ├── settings.py                          #爬虫详细配置案例
│   └── spiders
│       └── __init__.py
│       └── baidu_search.py       #爬虫实战：反爬百度搜索找到自己
│       └── baidu_splash.py       #爬虫实战：爬取百度动态js
│       └── ip138.py              #爬虫实战：伪装headers构造假IP骗过ip138.com
│       └── proxy_pool.py         #爬虫实战：教你打造自己的IP代理池
│       └── csdn_2018_blogstar.py #爬虫实战：大数据预测CSDN2018博客之星评选结果
│       └── qq_video.py           #爬虫实战：爬取腾讯视频评论生成词云图
│       └── taobao_splash.py      #爬虫实战：爬取淘宝动态页面内容
│       └── zhihu.py              #爬虫实战：Selenium登录知乎保存cookies后访问需要登录页面
└── scrapy.cfg
└── chromedriver                            #这个请自己按需下载
└── requirements.txt                        #工程运行依赖包
└── selenium_12306_ticket.py                #扫描模式自动刷票脚本
└── selenium_12306_ticket_exact_mode.py     #精确模式自动刷票脚本
```

## 精彩博客
- [Scrapy爬虫实战：百度搜索找到自己](https://blog.csdn.net/weixin_43430036/article/details/84840614)
- [scrapy爬虫实战：伪装headers构造假IP骗过ip138.com](https://blog.csdn.net/weixin_43430036/article/details/84849686)
- [Scrapy Selenium实战：Selenium登录知乎保存cookies后访问需要登录页面](https://blog.csdn.net/weixin_43430036/article/details/84871624)
- [大数据预测CSDN2018博客之星评选结果](https://blog.csdn.net/weixin_43430036/article/details/84944372)

## 精彩时刻
### 爬取腾讯视频评论生成词云图效果图
![效果图](https://github.com/Jaysong2012/tutorial/blob/master/backend/scripts/qq_video.png)

### CSDN 2018博客之星 所有参选作者自荐描述擅长词云图 
![效果图](https://github.com/Jaysong2012/tutorial/blob/master/backend/scripts/csdn_2018_blogstar_wordcloud.png)

## 刷票时刻
### 脚本说明
扫描模式自动刷票脚本 和 精确模式自动刷票脚本 核心流程原理都一样：利用selenium来模拟真实浏览器，将所有的人工操作都转换为机器自动化完成。

`selenium_12306_ticket.py`脚本的核心在于如果当前票已经卖光了，我们还是想买这张票，就可以利用这个脚本不断的尝试刷票购买，因为`selenium`模拟取网站信息比较慢，我这里利用了协程来加速扫描速度，只要扫描到了我们的票就立即跳转购买了。`selenium_12306_ticket.py`脚本可以配置多车次，多席位，多用户选择。

`selenium_12306_ticket_exact_mode.py`脚本的核心在于它只会精确的刷我们关心的车次，所以它的速度比`selenium_12306_ticket.py`全车次扫描脚本要快的多，因为目前春运的票还没有开始售卖，所以所有的人应该想用的是这个本脚本也支持多席位，多用户。

### 运行要求
请按照本博客要起[Scrapy Selenium实战：Selenium登录知乎保存cookies后访问需要登录页面](https://blog.csdn.net/weixin_43430036/article/details/84871624)搭建selenium环境
### 运行精确模式自动刷票脚本
```shell
python3 selenium_12306_ticket_exact_mode.py
```
刷票效果如下
```shell
2018-12-26 16:51:18 开始读取配置文件
2018-12-26 16:51:18 配置文件读取成功
2018-12-26 16:51:18 开始加载全部城市列表
2018-12-26 16:51:18 全部城市列表读取成功
2018-12-26 16:51:18 开始下载当前12306全部车次信息，50M左右，下载时间比较长，请耐心等待
/data/code/python/venv/venv_Scrapy/lib/python3.7/site-packages/urllib3/connectionpool.py:847: InsecureRequestWarning: Unverified HTTPS request is being made. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
  InsecureRequestWarning)
2018-12-26 16:51:21 下载当前12306全部车次信息，50M左右，下载完成
2018-12-26 16:51:22 系统配置读取完成
   您将为 ['张三', '李四'] 购买在 '2018-12-29' 由 广州 开往 武昌 的列车
   系统将选择 G94 列车的 ['二等座', '一等座'] 席位
2018-12-26 16:51:22 准备完成即将开始购票
2018-12-26 16:51:25 开始进入登录页面
2018-12-26 16:51:25 等待扫码登录登录码加载完成
2018-12-26 16:51:25 系统目前启用扫码登录，请打开手机12306客户端完成扫码登录，启用账户密码的方式为修改为 code_login 为 False
请检查网页是否有图形验证码需要点击，需要就请在在网页点击验证码图片，点击完成后，控制台输入1回车；如果无需点击验证码，则直接

......


2018-12-26 17:16:29 等待登录完成
2018-12-26 17:16:30 等待车票按钮显示完成
2018-12-26 17:16:30 自动将鼠标放到车票按钮上
2018-12-26 17:16:30 等待单程按钮显示完成
2018-12-26 17:16:31 自动点击单程按钮，加载查询车票页
2018-12-26 17:16:32 等待查询车票页面加载完成
2018-12-26 17:16:33 自动填充购票车站信息
2018-12-26 17:16:33 将开始发起查询
2018-12-26 17:16:33 点击查询按钮并且等待恢复可点击状态(等待查询完成)
2018-12-26 17:16:34 车票信息查询成功
2018-12-26 17:16:34 查票成功跳转到购买页
2018-12-26 17:16:34 等待乘车人列表加载完成
2018-12-26 17:16:36 自动选择乘车人 张三
2018-12-26 17:16:36 自动选择乘车人 李四
2018-12-26 17:16:36 自动选择座位类型，目前可选择的座位类型有 ['二等座（￥463.5）', '一等座（￥738.5）', '商务座（￥1458.5）']
2018-12-26 17:16:36 为 张三 自动选择座位类型，目前为你成功选择座位类型为 二等座
2018-12-26 17:16:36 自动选择座位类型，目前可选择的座位类型有 ['二等座（￥463.5）', '一等座（￥738.5）', '商务座（￥1458.5）']
2018-12-26 17:16:36 为 李四 自动选择座位类型，目前为你成功选择座位类型为 二等座
2018-12-26 17:16:36 自动点击提交购票按钮
2018-12-26 17:16:37 等待确认购买按钮加载完成
2018-12-26 17:16:37 自动点击确认购买按钮
完成购买！请在30分钟内登录账户，完成付款,点击Enter退出购票
```

