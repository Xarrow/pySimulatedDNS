# -*- coding:utf-8 -*-

"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: 1.py
 Time: 2017/7/16 20:14
"""
import logging
import socket
import threading
import sys

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)
PY3 = False

if sys.version > '3':
    PY3 = True
    import binascii

# 全局本地缓存
magic_cache = {'myip': '127.0.0.1'}


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


def parseDNSRQ(data):
    """解析DNSRQ报文"""

    # 是否需要三方DNS解析标识
    need_third_dns = True
    # byte 原始数据转化成十六进制字符串
    if PY3:
        request_hex_string = binascii.hexlify(data).decode('utf-8')
    else:
        request_hex_string = data.encode('hex')
    # 解析出域名
    domain, end = hex2domain(request_hex_string)
    logger.info("[+] DNS RQ:%s =====> %s", request_hex_string, domain)
    ip = None

    if domain and len(domain) > 0:
        # 获取主域名
        main_domain = domain.split('.')[-3]
        ip = magic_cache.get(main_domain)
        if ip:
            logger.info("%s From Cache  =====> %s", main_domain, ip)
        # 简单的做一下匹配
        if domain.__contains__('google') | \
                domain.__contains__("youtube") | \
                domain.__contains__("ytimg") | \
                domain.__contains__("gstatic") | \
                domain.__contains__("ggpht"):
            # sniproxy IP
            # 219.76.4.70
            ip = "61.91.161.217"
        if domain.__contains__("googlevideo"):
            ip = "183.91.33.46"
        if domain.__contains__("twitter") | \
                domain.__contains__("twimg") | \
                domain.__contains__("t.co"):
            ip = "104.224.140.135"
            # logger.info("[+] 翻墙 DNS IP 映射:%s =====> %s", domain, ip)

    response_hex_byte = None
    if ip:
        need_third_dns = False
        # ID标识+'81800001000100000000'+hex(域名)+00010001c00c000100010000003f0004'+hex(IP)
        response_hex_string = request_hex_string[0:4] + '81800001000100000000' + request_hex_string[
                                                                                 24:end] + '00010001c00c000100010000003f0004'
        # 十进制表示的IP变为十六进制表示的IP
        dnsip = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip.split('.'))).lower()
        response_hex_string += dnsip
        logger.info("[+] DNS IP 映射 : %s =====> %s ", domain, str(ip))
        if PY3:
            response_hex_byte = binascii.unhexlify(bytes(response_hex_string, 'utf-8'))
        else:
            response_hex_byte = response_hex_string.decode('hex')
    return need_third_dns, response_hex_byte


def call_remote_dns(udp, reqData, address,remote_dns='119.29.29.29'):
    """
        udp     主udp
        reqData 请求原始数据
        address 本地地址
        调用远程DNS服务器
    """

    sock_remote = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 请求腾讯DNS
    sock_remote.sendto(reqData, (remote_dns, 53))
    sock_remote.settimeout(5)
    resData = sock_remote.recv(1024)

    udp.sendto(resData, address)


def dispatch(udp, reqData, address):
    """中间分发"""
    need_third_dns, result_data = parseDNSRQ(data=reqData)
    if need_third_dns:
        call_remote_dns(udp, reqData, address)
    else:
        udp.sendto(result_data, address)


if __name__ == '__main__':
    logger.info("==========pySimulatedDNS=======")
    udp_local = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_local.bind(("0.0.0.0", 53))
    while True:
        try:
            reqData, address = udp_local.recvfrom(5120)
            t = threading.Thread(target=dispatch, args=(udp_local, reqData, address))
            t.setDaemon(True)
            t.start()

            logger.info("当前活动线程数:%s", threading.activeCount())
        except Exception as ex:
            logger.error("===> 解析异常: %s", ex)
            pass
    pass
