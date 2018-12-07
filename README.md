# scrapy实战项目
## tutorial项目结构
```
tutorial/
├── backend                                  #后端辅助demo模块
│   ├── __init__.py 
│   └── libs                                 #自写代码工具类模块
│   └── models                               #数据库模型模块 
│   └── scripts                              #其他单独脚本模块
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
│       └── qq_video.py           #爬虫实战：爬取腾讯视频评论生成词云图
│       └── taobao_splash.py      #爬虫实战：爬取淘宝动态页面内容
│       └── zhihu.py              #爬虫实战：Selenium登录知乎保存cookies后访问需要登录页面
└── scrapy.cfg
```

## 精彩博客
- [Scrapy爬虫实战：百度搜索找到自己](https://blog.csdn.net/weixin_43430036/article/details/84840614)
- [scrapy爬虫实战：伪装headers构造假IP骗过ip138.com](https://blog.csdn.net/weixin_43430036/article/details/84849686)
- [Scrapy Selenium实战：Selenium登录知乎保存cookies后访问需要登录页面](https://blog.csdn.net/weixin_43430036/article/details/84871624)

## 精彩时刻
### 爬取腾讯视频评论生成词云图效果图
![效果图](https://github.com/Jaysong2012/tutorial/blob/master/backend/scripts/qq_video.png)
