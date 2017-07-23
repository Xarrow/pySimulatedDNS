# -*- coding:utf-8 -*-


"""
 Verion: 1.0
 Author: zhangjian
 Site: http://iliangqunru.com
 File: pySimulatedDNS_Beta.py
 Time: 2017/7/23 18:01
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

# =========================================
def get_ip_from_google(domain):
    """获取googleDNS"""
    import requests
    google_dns_json_result = requests.get('https://dns.google.com/resolve?name=' + domain).json()
    answer = google_dns_json_result['Answer']
    if len(answer) > 0:
        data_string = answer[-1]['data']
        magic_cache[domain] = data_string
        return domain, data_string
    pass


def get_ip_by_domain(domain):
    """根据域名获取ip"""
    ip = magic_cache.get(domain)
    if not ip:
        return get_ip_from_google(domain)
    return domain, ip


def struct_dns_response(domain, ip, request_hex_string, end):
    """构造dns响应"""
    # ID标识+'81800001000100000000'+hex(域名)+00010001c00c000100010000003f0004'+hex(IP)
    response_data_hex = request_hex_string[0:4] + '81800001000100000000' + request_hex_string[
                                                                           24:end] + '00010001c00c000100010000003f0004'
    # 十进制表示的IP变为十六进制表示的IP
    dnsip = '{:02X}{:02X}{:02X}{:02X}'.format(*map(int, ip.split('.'))).lower()
    # print "Revise:\t", domain
    response_data_hex += dnsip
    logger.info("[+] DNS IP 映射 : %s =====> %s ", domain, str(ip))

    if PY3:
        response_hex_byte = binascii.unhexlify(bytes(response_data_hex, 'utf-8'))
    else:
        response_hex_byte = response_data_hex.decode('hex')
    return response_hex_byte


def core_service(udp_socket, data, address):
    # 原始请求数据十六进制字符串
    if PY3:
        request_hex_string = binascii.hexlify(data).decode('utf-8')
    else:
        request_hex_string = data.encode('hex')
    # 解析出域名
    domain, end = hex2domain(request_hex_string)
    if domain and len(domain) > 0:
        # 获取域名ip
        _domain, ip = get_ip_by_domain(domain)
        # 构造响应报文
        response_hex_byte = struct_dns_response(_domain, ip, request_hex_string, end)
        # 发送DNS报文
        udp_socket.sendto(response_hex_byte, address)

if __name__ == '__main__':
    pass