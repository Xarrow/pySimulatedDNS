# -*- coding:utf-8 -*-


"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: socket_test.py
 Time: 2017/8/30 16:52
"""
import logging
import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
import binascii
import socket


def send_raw_dns(domain):
    raw_msg = binascii.unhexlify(
        bytes(
            "34f801000001000000000000036d3130056d7573696303313236036e65740000010001",
            # "0eb8010000010000000000000c" + binascii.hexlify(bytes(domain, 'utf-8')).decode('utf-8') + "0000010001",
            'utf-8'))
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(raw_msg, ('127.0.0.1', 54))
    res_data = udp_socket.recv(1024)
    logger.info('==> %s', res_data)


if __name__ == '__main__':
    send_raw_dns("baidu.com")
    pass
