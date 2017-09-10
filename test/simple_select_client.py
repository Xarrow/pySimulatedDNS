# -*- coding:utf-8 -*-


"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: simple_select_client.py
 Time: 2017/9/9 20:54
"""
import logging
import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

import socket
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.connect(('127.0.0.1',5555))

socket.sendall(b"dir")
server_data = socket.recv(1024)
logger.info("data from server is :%s",server_data)