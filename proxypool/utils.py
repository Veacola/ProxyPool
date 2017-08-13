import requests
import asyncio
import aiohttp
from requests.exceptions import ConnectionError
from proxypool.logger import Logger

base_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8'
}


def get_page(url, options={}):
    headers = dict(base_header, **options)
    Logger.log_normal('Getting %s' % url)
    try:
        r = requests.get(url, headers=headers)
        Logger.log_high('Getting result %s %s' % (url, r.status_code))
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        Logger.log_fail('Crawling Failed %s' % url)
        return None


if __name__ == '__main__':
    result = get_page('http://www.goubanjia.com/free/gngn/index.shtml')
    print(result)
