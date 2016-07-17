# -*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
from selenium import webdriver
#该模块执行具体的数据爬取操作！


class Browser:
    ''' browser基于phantomJS 需要安装phantomJS
        实现基本的网页获取
    '''
    browser = None

    def __init__(self):
        ''' 配置phantomJS
            设置超时时间
            禁止加载图片及Agent
            然后初始化webdriver'''
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.userAgent'] = 'faking it'
        if self.browser is None:
            self.browser = webdriver.PhantomJS(desired_capabilities=cap)

    def renderPage(self, url):
        '''获取指定url的网页源代码'''
        self.browser.get(url)
        return self.browser.page_source

    def queryResult(self, url):
        ''' 根据自己的规则来进行数据的查找
            返回需要的数据类型。
            返回应设置为list(用于url的存储)
            或者dict(用于具体数据的存储)'''
        htmldoc = pq(self.renderPage(url))
        if 'templatemonster' in url:
            return monster(htmldoc, url)

    def restart(self):
        ''' 由于phantomJS的一个memory leak(内存泄漏)
            在执行玩一个页面之后对phantomjs执行重启操作
            如果不是在服务器上，使用chrome则不存在这个问题
            该方法节约了内存但是很大程度上的降低了效率'''
        if self.browser is not None:
            self.quit()
            self.browser = None
        self.__init__()

    def quit(self):
        '''推出浏览器'''
        self.browser.quit()


def monster(htmldoc, url):
    ''' 该函数是根据某一个网站的结构所做的规则函数
        该函数在browser内被调用
        要么返回urllisit(针对信息列表页面)
        要么返回dict类型的数据信息
        这里将用的数据信息将用title做主key'''
    #pyquery的语法
    linksobj = htmldoc('#products .small-prev-data a')
    links = []
    if len(linksobj) != 0:
        for linkobj in linksobj:
            links.append(pq(linkobj).attr('href'))
        return links
    if len(links) == 0:
        title = pq(htmldoc('.page-heading h1')).text()
        preview = pq(htmldoc('.buttons-wrapper a')[0]).attr('href')
        download =
        return {'title': title, 'preview': preview, 'download': download}
