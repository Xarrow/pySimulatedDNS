# -*- coding:utf-8 -*-


"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: hex_tools.py
 Time: 2017/8/30 15:23
"""
import logging
import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
import binascii


def _hex_to_ascii(hex_object):
    """hex to ascii chr"""
    if hex_object.__class__ == bytes:
        hex_object = str(hex_object, 'utf-8')
    Int = int(hex_object, 16)
    return chr(Int)


def _ascii_chr_to_hex(ascii_chr, ret_type='bytes'):
    """ascii string to hex string
        单个chr转十六进制string,默认返回bytes类型,可选择返回string
    """
    if ascii_chr.__class__ == bytes:
        _hex_bytes_data = binascii.hexlify(ascii_chr)
    else:
        _hex_bytes_data = binascii.hexlify(bytes(ascii_chr, 'utf-8'))
    if ret_type == 'string':
        return _hex_bytes_data.decode('utf-8')
    return _hex_bytes_data


def _hex_to_decimal(hex_string):
    """hex string to decimal string"""
    pass


if __name__ == '__main__':
    logger.info("==> %s", _hex_to_ascii("32"))
    logger.info("==> %s", _hex_to_ascii(b"32"))
    logger.info("==> %s", _ascii_chr_to_hex(b"2"))
    logger.info("==> %s", _ascii_chr_to_hex(b"2", ret_type='string'))
