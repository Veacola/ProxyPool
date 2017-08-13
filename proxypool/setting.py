"""
-------------------------------------------------
    File Name:      setting.py
    Description:    设置模块，包含一些常量。
    Learner:        Xiaopeng Guo
    Copyright:      WiseDoge
-------------------------------------------------
"""

# Redis数据库的地址和端口
HOST = 'localhost'
PORT = 6379


# 如果Redis有密码限制，添加这句密码，否则设置为None
PASSWORD = 'ah3rcj93'


# 代理池数量界限
POOL_LOWER_THRESHOLD = 10
POOL_UPPER_THRESHOLD = 10000


# 检查周期
VALID_CHECK_CYCLE = 10
POOL_LEN_CHECK_CYCLE = 5


# 测试API,用百度来测试
TEST_API_BAIDU = 'https://www.baidu.com'
