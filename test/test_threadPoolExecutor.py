# -*- coding:utf-8 -*-


"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: test_threadPoolExecutor.py
 Time: 2017/9/3 0:31
"""
import logging
import threading

import requests

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
import time


def timer(func):
    def wrapper(*args, **kwargs):
        start = int(time.time() * 1000)
        rs = func(*args, **kwargs)
        end = int(time.time() * 1000)
        logger.info("==> %s timer is :%sms", args, (end - start))
        return rs

    return wrapper


@timer
def handle_requests(url):
    r = requests.get(url=url)
    return r.url

urls = ['http://www.python.org',
        'http://www.python.org/about/',
        'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
        'http://www.python.org/doc/',
        'http://www.python.org/download/',
        'http://www.python.org/getit/',
        'http://www.python.org/community/',
        'https://wiki.python.org/moin/',
        'http://planet.python.org/',
        'https://wiki.python.org/moin/LocalUserGroups',
        'http://www.python.org/psf/',
        'http://docs.python.org/devguide/',
        'http://www.python.org/community/awards/']


def test_threadpoolExecutor():
    """test threadpoolExecutor"""
    pool = ThreadPoolExecutor(20)
    for url in urls:
        future = pool.submit(handle_requests, (url))
        future


def test_threading():
    for url in urls:
        t = threading.Thread(target=handle_requests, args=(url,))
        t.start()
        t.join()


import queue

q = queue.Queue(20)


def test_queue_get():
    while True:
        if q.empty():
            break
        item = q.get()
        handle_requests(item)


def test_queue_put():
    for url in urls:
        q.put(url)


import threading


@timer
def single_thread():
    t = threading.Thread(target=handle_requests, args=("https://iliangqunru.com",))
    t.start()


if __name__ == '__main__':

    # for url in urls:
    #     t = threading.Thread(target=handle_requests,args=(url,))
    #     t.start()

    # start = int(time.time() * 1000)
    # test_threadpoolExecutor()
    # test_threading()
    # test_queue_put()
    # test_queue_get()
    # single_thread()
    # end = int(time.time() * 1000)
    # logger.info("===> final timer is %sms", (end - start))
    pass
