# -*- coding:utf-8 -*-


"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: simple_ss_client.py
 Time: 2017/9/15 上午1:53
"""
import logging
import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

PY3 = False
if sys.version > '3.':
    PY3 = True


def func():
    pass


class Main():
    def __init__(self):
        pass

import socks

if __name__ == '__main__':
    s =socks.socksocket()
    s.setproxy(socks.SOCKS5,"localhost",8888)
    s.connect(("https://baidu.com",443))
    s.sendall(b"GET / HTTP/1.1 /r/n/r/n")
    logger.info("==> %s",s.recv(2048))
