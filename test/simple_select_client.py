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
import threading




level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
import socket

message_list = ["hello", "world", "i", "am", "socket"]
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('104.224.140.135', 5555))

socket.send("ls -l video")
logger.info("==> %s",socket.recv(1024))
# for msg in message_list:
#     socket.send(bytes(msg))
#     server_data = socket.recv(1024)
#     logger.info("data from server is :%s", server_data)
