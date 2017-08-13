"""
-------------------------------------------------
    File Name:      db.py
    Description:    数据库操作模块，负责对象与底层数据库
                    的交互。
    Learner:        Xiaopeng Guo
    Copyright:      WiseDoge
-------------------------------------------------
"""
import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import HOST, PORT, PASSWORD


class RedisClient(object):
    '''
    Redis数据库操作类
    '''
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            pool = redis.ConnectionPool(
                host=host, port=port, db=1, password=PASSWORD)
            self._db = redis.Redis(connection_pool=pool)
        else:
            pool = redis.ConnectionPool(host=host, port=port, db=1)
            self._db = redis.Redis(connection_pool=pool)

    def get(self, count=1):
        '''从Pool中获取一定量的代理数据'''
        proxies = self._db.lrange("proxies", 0, count-1)
        self._db.ltrim("proxies", count, -1)
        return proxies

    def put(self, proxy):
        '''在list最右侧添加代理数据'''
        self._db.rpush("proxies", proxy)

    def put_many(self, proxies):
        """将一定量的代理压入Pool"""
        for proxy in proxies:
            self.put(proxy)

    def pop(self):
        '''从list最右侧取出代理数据并在池中移除'''
        try:
            return self._db.rpop("proxies").decode('utf-8')
        except:
            raise PoolEmptyError

    @property
    def queue_len(self):
        '''获取proxy pool的大小'''
        return self._db.llen("proxies")

    def flush(self):
        '''刷新Redis中的全部内容，测试用'''
        self._db.flushall()


if __name__ == '__main__':
    conn = RedisClient()
    print(conn.pop())
