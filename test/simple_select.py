# -*- coding:utf-8 -*-


"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: simple_select.py
 Time: 2017/9/9 20:29
"""
import logging
import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

import select
import socket
import sys

import commands

sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0',5555))
sock.listen(5)

while True:
    client_socket ,client_address = sock.accept()
    logger.info("==> new connect from %s",client_address)
    client_socket.setblocking(0)
    client_data = client_socket.recv(10240)
    if client_data:
        logger.info("==> data from client is :%s",client_data)
        client_socket.send(commands.getoutput(client_data))
    client_socket.close()


# server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_sock.bind(("0.0.0.0", 5555))
# server_sock.listen(5)
# inputs = [server_sock]
# outputs = []
# errorList = []
# while True:
#     readable, wirtable, errorable = select.select(inputs, outputs, [])
#     for server in readable:
#         client_socket, client_address = server.accept()
#         inputs.append(server_sock)
#         outputs.append(server_sock)
#         for i in outputs:
#             i.send(b"hello world")
#             i.shutdown(flag="SHUT_WR")
