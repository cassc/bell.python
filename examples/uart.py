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


def isBlank (myString):
    return not (myString and myString.strip())

def isNotBlank (myString):
    return bool(myString and myString.strip())

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


msg_id = 0;

ser.isOpen()

# 处理收到的BASE64编码的数据
def print_handler(msg):
    if isBlank(msg):
        return
    print('Recv raw msg: {}'.format(msg))
    v = json.loads(base64.urlsafe_b64decode(msg.encode('utf-8')).decode('utf-8'))
    print('Recv json msg: {}'.format(v))

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

def test_msg():
    print('results 1: {}'.format(parse_for_msg(':ABC;\n', print_handler)))
    print('results 2: {}'.format(parse_for_msg('ABC;\n:BBBB;\n', print_handler)))
    print('results 3: {}'.format(parse_for_msg(':AAA;\n:BBBB;\n', print_handler)))
    print('results 4: {}'.format(parse_for_msg(':CAAAA', print_handler)))
    print('results 5: {}'.format(parse_for_msg(':CAAAA;\n__', print_handler)))
    print('results 6: {}'.format(parse_for_msg(':CAAAA;\n', print_handler)))
    print('results 7: {}'.format(parse_for_msg('\n:AAA', print_handler)))

def start_msg_reader():
    out = '';
    while True:
        while ser.inWaiting() > 0:
            try:
                out += ser.read(1).decode('utf-8')
                out = parse_for_msg(out, print_handler)
            except Exception as e:
                print(e)
                    
thread.start_new_thread(start_msg_reader, ())

while True :
    msg_id = msg_id +1
    msg_buf = ""
    msg = json.dumps({"from":   "ui",
                      "tpe":    "wstatus",
                      "target": "be"})

    print("send: {}".format(msg))
    # 组包并发送
    ss = ':' + base64.urlsafe_b64encode(msg.encode('utf-8')).decode('utf-8') + ';'
    ser.write(ss.encode('utf-8'))

    time.sleep(5)

    
    

