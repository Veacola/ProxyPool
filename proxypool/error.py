"""
-------------------------------------------------
    File Name:      error.py
    Description:    异常模块
    Learner:        Xiaopeng Guo
    Copyright:      WiseDoge
-------------------------------------------------
"""


class ResourceDepletionError(Exception):
    """
    资源枯竭异常，如果从所有网站都抓不到可用的代理资源，
    则抛出该异常。
    """

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy source is exhausted')


class PoolEmptyError(Exception):
    """
    代理池空异常，如果代理池长时间为空，则抛出此异常。
    """
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('The proxy pool is empty')
