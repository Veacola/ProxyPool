"""
-------------------------------------------------
    File Name:      schedule.py
    Description:    调度器模块，
                    包含VaildityTester, PoolAdder,
                    Schedule三个类，负责维护代理池。
    Learner:        Xiaopeng Guo
    Copyright:      WiseDoge
-------------------------------------------------
"""
import time
from multiprocessing import Process
import asyncio
import aiohttp
try:
    from aiohttp.errors import ProxyConnectionError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.error import ResourceDepletionError
from proxypool.getter import FreeProxyGetter
from proxypool.setting import *
from proxypool.logger import Logger
from asyncio import TimeoutError


class VaildityTester(object):
    """
    检验器，负责对未知的代理进行异步检测。
    """
    test_api = TEST_API_BAIDU

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        """
        设置待检测的代理。
        """
        self._raw_proxies = proxies
        self._conn = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        检测单个代理，如果可用，则将其加入_usable_proxies
        """
        async with aiohttp.ClientSession() as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                Logger.log_normal('Testing %s' % proxy)
                async with session.get(
                        self.test_api, proxy=real_proxy, timeout=15) as resp:
                            if resp.status == 200:
                                self._conn.put(proxy)
                                Logger.log_high('Valid proxy %s' % proxy)
            except Exception:
                pass

    def test(self):
        """
        异步检测_raw_proxies中的全部代理
        """
        Logger.log_normal('VaildityTester is working')
        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy)
                     for proxy in self._raw_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
        except ValueError:
            Logger.log_fail('Async Error')

    def get_usable_proxies(self):
        return self._usable_proxies


class PoolAdder(object):
    """
    添加器，负责向池中补充代理
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()
        self._tester = VaildityTester()
        self._crawler = FreeProxyGetter()

    def is_over_threshold(self):
        """
        判断代理池中的数量是否达到阈值
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        """
        命令爬虫抓取一定量未检测的代理，然后检测，将通过检测的代理加入到代理池中
        """

        Logger.log_normal('PoolAdder is working')
        proxy_count = 0
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):
                callback = self._crawler.__CrawlFunc__[callback_label]
                raw_proxies = self._crawler.get_raw_proxies(callback)

                # test crawled proxies
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()

                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    Logger.log_high('IP is enough, waiting to be used')
                    break
                if proxy_count == 0:
                    raise ResourceDepletionError


class Schedule(object):
    @staticmethod
    def valid_proxy(cycle=VALID_CHECK_CYCLE):
        """从redis里面获取一半的代理
        """
        conn = RedisClient()
        tester = VaildityTester()
        while True:
            Logger.log_high('Refreshing ip')
            count = int(0.5 * conn.queue_len)
            if count == 0:
                Logger.log_normal('Waiting for adding')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    @staticmethod
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD,
                   upper_threshold=POOL_UPPER_THRESHOLD,
                   cycle=POOL_LEN_CHECK_CYCLE):
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    def run(self):
        Logger.log_high('Ip processing running')
        valid_process = Process(target=Schedule.valid_proxy)
        check_process = Process(target=Schedule.check_pool)
        valid_process.start()
        check_process.start()
