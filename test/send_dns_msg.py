# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: send_dns_msg.py
 Time: 2017/8/29 20:14
"""
import logging
import socket
import threading
import select
from concurrent.futures import ThreadPoolExecutor


level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
PY3 = False
import binascii

BUFFER_SIZE = 2048
CACHE = dict()


def log_req_res(func):
    '''
    drop
    :param func:
    :return:
    '''
    logger.info("function name is %s", func.__name__)

    def wrapped(*args, **kwargs):
        logger.info("req hex ==> %s", str(kwargs))
        result = func(*args, **kwargs)
        logger.info("res hex ==> %s", str(result))

    return wrapped


import struct


def hex2ascii(string):
    try:
        Int = int(string, 16)
        return chr(Int)
    except Exception as e:
        logger.error("Hex2Ascii info:", e)


def hex2domain(string, start=24, end=26):
    """将原始十六进制报文字符串解析出域名，默认从24-26字节位置开始"""
    try:
        domain = []
        while string[start:end] != '00' and string[start:end] != 'c0':
            n = 0
            i = int(string[start:end], 16)
            while n < i:
                start = end
                end += 2
                domain.append(hex2ascii(string[start:end]))
                n += 1
            domain.append(".")
            start = end
            end += 2
        return ''.join(domain), end
    except Exception as ex:
        logger.error("hex2domain info:", ex)
        pass


def parse_rq_rs_data(req_data, res_data):
    req_hex_string = binascii.hexlify(req_data).decode('utf-8')
    res_hex_string = binascii.hexlify(res_data).decode('utf-8')

    domain, end = hex2domain(req_hex_string)
    long_hex_ip = res_hex_string[-8:]
    addr_long = int(long_hex_ip, 16)
    ip_str = socket.inet_ntoa(struct.pack("<L", addr_long))

    if domain.__contains__('google') | \
            domain.__contains__("youtube") | \
            domain.__contains__("ytimg") | \
            domain.__contains__("gstatic") | \
            domain.__contains__("ggpht"):
        # sniproxy IP
        # 219.76.4.70
        ip_str = "61.91.161.217"
    logger.info("%s ==> %s", domain, ip_str)
    CACHE[domain] = ip_str
    pass


def send_third_dns(req_data, remote_dns="8.8.8.8"):
    '''
    get res_data from third dns
    :param req_data:
    :param remote_dns:
    :return:
    '''
    logger.info("raw rq ==> %s", req_data)
    logger.info("hex rq ==> %s", binascii.hexlify(req_data).decode('utf-8'))
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    remote_socket.sendto(req_data, (remote_dns, 53))
    remote_socket.settimeout(5)
    res_data = remote_socket.recv(BUFFER_SIZE)
    logger.info("raw rs ==> %s", res_data)
    logger.info("hex rs ==> %s", binascii.hexlify(res_data).decode('utf-8'))
    # parse response data
    try:
        parse_rq_rs_data(req_data, res_data)
    except Exception as e:
        pass
    return res_data


def packingMsg(req_data, end, cache_ip):
    request_hex_string = binascii.hexlify(req_data).decode('utf-8')
    # ID标识+'81800001000100000000'+hex(域名)+00010001c00c000100010000003f0004'+hex(IP)
    response_hex_string = request_hex_string[0:4] + '81800001000100000000' \
                          + request_hex_string[24:end] + '00010001c00c000100010000003f0004'
    # 十进制表示的IP变为十六进制表示的IP
    dnsip = binascii.hexlify(socket.inet_aton(cache_ip)).decode('utf-8')
    # dnsip = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, cache_ip.split('.'))).lower()
    response_hex_string += dnsip
    res_data = binascii.unhexlify(bytes(response_hex_string,'utf-8'))
    return res_data
    # if PY3:
    #     response_hex_byte = binascii.unhexlify(bytes(response_hex_string, 'utf-8'))
    # else:
    #     response_hex_byte = response_hex_string.decode('hex')
    # pass


def switch(local_udp, req_data, address):
    domain, end = hex2domain(binascii.hexlify(req_data).decode('utf-8'))
    cache_ip = CACHE.get(domain)
    # if cache_ip:
    #     # packet msg
    #     logger.info("[SWITCH2CACHE] %s ==> %s", domain, cache_ip)
    #     res_data = packingMsg(req_data, end, cache_ip)
    # else:
    #     # request third dns server
    #     logger.info("[SWITCH2DNS] ==> %s", domain, )
    #     res_data = send_third_dns(req_data=req_data)
    logger.info("[SWITCH2DNS] ==> %s", domain, )
    if domain.endswith('.net.') or domain.endswith('.cn.'):
        res_data = send_third_dns(req_data=req_data,remote_dns='8.8.8.8')
    else:
        res_data = send_third_dns(req_data=req_data)
    r,w,e = select.select([],[local_udp],[],5)
    if len(w)!=0:
        local_udp.sendto(res_data, address)
    # local_udp.sendto(req_data,address)
    pass


if __name__ == '__main__':
    pool = ThreadPoolExecutor(11)
    local_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_udp.bind(("127.0.0.1", 54))
    while True:
        try:
            infds,outfds,errds = select.select([local_udp,],[],[],5)
            if len(infds)!=0:

                for so in infds:
                    if so is socket:
                        req_data , address= so.recvfrom(BUFFER_SIZE)
                        switch(so,req_data,address)

            # req_data, address = local_udp.recvfrom(BUFFER_SIZE)
            # task = pool.submit(switch,local_udp,req_data,address)

            # t = threading.Thread(target=switch, args=(local_udp, req_data, address))
            # t.setDaemon(True)
            # t.start()
            logger.info("current thread count is :%d", threading.activeCount())
            logger.info("current thread enumerate is :%d", len(threading.enumerate()))
        except Exception as e:
            pass

