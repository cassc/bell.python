# coding: utf-8
from threading import Thread
import time
import serial
import json
import base64
import re
try:
    import thread
except ImportError:
    import _thread as thread


# 串口连接    
ser = None
    
def isBlank (myString):
    return not (myString and myString.strip())

def isNotBlank (myString):
    return bool(myString and myString.strip())

# 处理收到的BASE64编码的数据
def print_handler(msg):
    from pprint import pprint
    if isBlank(msg):
        return
    pprint('Recv raw msg: {}'.format(msg))
    v = json.loads(base64.urlsafe_b64decode(msg.encode('utf-8')).decode('utf-8'))
    pprint(v)

# 对收到的数据拆分与组包
def parse_for_msg(ss, handler):
    lines = ss.split('\n')
    if len(lines) == 0:
        return ""
    last_line = ''
    for line in lines:
        if line.startswith(':') and line.endswith(';'):
            handler(line[1:-1])
            last_line = lines[-1]
        if last_line.startswith(':'):
            if last_line.endswith(';'):
                return ''
            return last_line
    return ss

# def test_msg():
#     print('results 1: {}'.format(parse_for_msg(':ABC;\n', print_handler)))
#     print('results 2: {}'.format(parse_for_msg('ABC;\n:BBBB;\n', print_handler)))
#     print('results 3: {}'.format(parse_for_msg(':AAA;\n:BBBB;\n', print_handler)))
#     print('results 4: {}'.format(parse_for_msg(':CAAAA', print_handler)))
#     print('results 5: {}'.format(parse_for_msg(':CAAAA;\n__', print_handler)))
#     print('results 6: {}'.format(parse_for_msg(':CAAAA;\n', print_handler)))
#     print('results 7: {}'.format(parse_for_msg('\n:AAA', print_handler)))

def start_msg_reader():
    out = '';
    while True:
        while ser.inWaiting() > 0:
            try:
                out += ser.read(1).decode('utf-8')
                out = parse_for_msg(out, print_handler)
            except Exception as e:
                print(e)


def send_request(req):
    msg = json.dumps(req)

    print('send: {}'.format(msg))
    # 组包并发送
    ss = ':' + base64.urlsafe_b64encode(msg.encode('utf-8')).decode('utf-8') + ';'
    ser.write(ss.encode('utf-8'))

def run():
    global ser

    # 打开串口
    # 这几个参数与主控一致
    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    while not ser.isOpen():
        print('等待连接')
        time.sleep(2)

    # 开启读线程
    thread.start_new_thread(start_msg_reader, ())

    # 查询主控wifi状态
    msg = {'from':   'ide',
           'tpe':    'wstatus',
           'nonce': '227',
           'target': 'be'}

    send_request(msg)

    time.sleep(3)


    # 上传脚本并执行
    with open('spiral.py', 'r') as f:
        prog_content= f.read()
    
    prog_title = 'copyball.py'
    msg = {'from':   'ide',
           'tpe':    'prog.upload',
           'nonce': '228',
           'target': 'be',
           'data': {'content':prog_content,
                    'title': prog_title,
                    'run': True,},}

    send_request(msg)

    time.sleep(20)
    
run()    

