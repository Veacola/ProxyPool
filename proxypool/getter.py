"""
-------------------------------------------------
    File Name:      getter.py
    Description:    代理抓取模块，负责与网络的交互。
                    注意，代理网站的HTML结构可能会时常的更新，
                    会导致本文件下的抓取函数失效，所以，在运行
                    代理池之前，需要更新一下FreeProxyGetter类
                    中以crawl_开头的方法。
    Learner:        Xiaopeng Guo
    Copyright:      WiseDoge
-------------------------------------------------
"""

import time
import random
import json
import requests
from proxypool.utils import get_page
from proxypool.logger import Logger
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    '''
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数分别表示爬虫函数和爬虫函数的数量
    '''
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):

    def get_raw_proxies(self, callback):
        proxies = []
        Logger.log_normal('Callback %s' % callback)
        for proxy in eval("self.{}()".format(callback)):
            Logger.log_normal('Getting %s from %s' % (proxy,callback))
            proxies.append(proxy)
        return proxies

    def crawl_daxiang(self):
        url = 'http://vtp.daxiangdaili.com/ip/?tid=556488478479034&num=1000'
        data = get_page(url)
        if data:
            data = data.split('\r\n')
            for proxy in data:
                if proxy:
                    yield proxy
    # def crawl_xundaili(self):
    #     url = 'http://www.xdaili.cn/ipagent/greatRecharge/getGreatIp?spiderId=a11e1bacebe5403198c7d8f14847e9ca&orderno=YZ20177231264JSpJYg&returnType=2&count=100'
    #     data = json.loads(get_page(url))
    #     if data:
    #             for proxy in data['RESULT']:
    #                 if proxy:
    #                     try:
    #                         print(type(proxy))
    #                         print(type(proxy['ip']))
    #                         print('-----------------------------------------------------')
    #                         ip = proxy['ip']
    #                         port = proxy['port']
    #                         yield ':'.join([ip, port])
    #                     except:
    #                         pass

    # def crawl_kuaidaili(self, page_count=10):
    #     start_url = 'http://www.kuaidaili.com/free/outha/{}/'
    #     urls = [start_url.format(page) for page in range(1, page_count + 1)]
    #     for url in urls:
    #         time.sleep(5)
    #         html = get_page(url)
    #         if html:
    #             doc = pq(html)
    #             trs = doc('#list table tr:gt(0)').items()
    #             for tr in trs:
    #                 ip = tr.find('td[data-title="IP"]').text()
    #                 port = tr.find('td[data-title="PORT"]').text()
    #                 yield ':'.join([ip, port])

    # def crawl_daili66(self, page_count=4):
    #     start_url = 'http://www.66ip.cn/{}.html'
    #     urls = [start_url.format(page) for page in range(1, page_count + 1)]
    #     for url in urls:
    #         print('Crawling', url)
    #         html = get_page(url)
    #         if html:
    #             doc = pq(html)
    #             trs = doc('.containerbox table tr:gt(0)').items()
    #             for tr in trs:
    #                 ip = tr.find('td:nth-child(1)').text()
    #                 port = tr.find('td:nth-child(2)').text()
    #                 yield ':'.join([ip, port])
                    
    # def crawl_haoip(self):
    #     start_url = 'http://haoip.cc/tiqu.htm'
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html)
    #         results = doc('.row .col-xs-12').html().split('<br/>')
    #         for result in results:
    #             if result:
    #                 yield result.strip()

    # def crawl_proxy360(self):
    #     start_url = 'http://www.proxy360.cn/Region/China'
    #     print('Crawling', start_url)
    #     html = get_page(start_url)
    #     if html:
    #         doc = pq(html)
    #         lines = doc('div[name="list_proxy_ip"]').items()
    #         for line in lines:
    #             ip = line.find('.tbBottomLine:nth-child(1)').text()
    #             port = line.find('.tbBottomLine:nth-child(2)').text()
    #             yield ':'.join([ip, port])

    # def crawl_goubanjia(self):
    #     start_url = 'http://www.goubanjia.com/free/gngn/index.shtml'
    #     html = get_page(start_url)
    #     if html:
    #         # 用PyQuery加载一段html
    #         doc = pq(html)

    #         # 获取所有的td.ip
    #         tds = doc('td.ip').items()
    #         for td in tds:
    #             td.find('p').remove()
    #             yield td.text().replace(' ', '')

if __name__ == '__main__':
    result = FreeProxyGetter()
    print(result.crawl_daxiang())
    # print(result.get_raw_proxies('crawl_kuaidaili'))
