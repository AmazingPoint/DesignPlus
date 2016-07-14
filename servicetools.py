# -*- coding: UTF-8 -*-
from pyquery import PyQuery as pq
from selenium import webdriver

SOURCE_HTML = ['http://www.doooor.com/forum-38-typeid15.html',
               'http://sc.chinaz.com/tag_moban/Html.html',
               'http://www.mobanwang.com/mb/']


class Browser:
    browser = None

    def __init__(self):
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap['phantomjs.page.settings.resourceTimeout'] = 1000
        cap['phantomjs.page.settings.loadImages'] = False
        cap['phantomjs.page.settings.userAgent'] = 'faking it'
        if self.browser is None:
            self.browser = webdriver.PhantomJS(desired_capabilities=cap)

    def renderPage(self, url):
        self.browser.get(url)
        return self.browser.page_source

    def queryResult(self, url):
        htmldoc = pq(self.renderPage(url))
        if 'doooor' in url:
            return doooor(htmldoc, url)
        if 'chinaz' in url:
            return chinaz(htmldoc, url)
        if 'mobanwang' in url:
            return mobanwang(htmldoc, url)

    def restart(self):
        if self.browser is not None:
            self.browser.quit()
            self.browser = None
        self.__init__()


def doooor(htmldoc, url):
    title = pq(htmldoc('title')).text()
    linksobj = htmldoc('#shoucang .scitem .simgh a')
    links = []
    if linksobj is not None:
        for linkobj in linksobj:
            links.append('http://www.doooor.com/' + pq(linkobj).attr('href'))

    if len(links) == 0:
        preview = pq(htmldoc('.mbn img')).attr('src')
        download = url
        return {'title': title, 'preview': preview, 'download': download}
    next_link_obj = None('.nxt')
    if len(next_link_obj) != 0:
        next_link = pq(next_link_obj).attr('href')
        links.append(next_link)
    return links


def chinaz(htmldoc, url):
    linksobj = htmldoc('#container .box div a')
    links = []
    if linksobj is not None:
        for linkobj in linksobj:
            links.append('http://sc.chinaz.com' + pq(linkobj).attr('href'))
    if len(links) == 0:
        preview = pq(htmldoc('.imga img')).attr('src')
        title = pq(htmldoc('.imga a')).attr('title')
        download = pq(htmldoc('.img_yl a')).attr('href')
        if download is not None:
            download = 'http://sc.chinaz.com' + download.strip()
        return {'title': title, 'preview': preview, 'download': download}
    next_link_obj = None('.nextpage')
    if len(next_link_obj) != 0:
        next_link = pq(next_link_obj).attr('href')
        next_link = next_link.replace('HTML', 'index')
        links.append('http://sc.chinaz.com/moban/' + next_link)
    return links


def mobanwang(htmldoc, url):
    title = pq(htmldoc('title')).text()
    linksobj = htmldoc('.divBoxH129 li a')
    links = []
    if linksobj is not None:
        for linkobj in linksobj:
            links.append(pq(linkobj).attr('href'))
    if len(links) == 0:
        preview = pq(htmldoc('.preview p img')).attr('src')
        download = url
        return {'title': title, 'preview': preview, 'download': download}
    return links
