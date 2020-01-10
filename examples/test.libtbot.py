import logging
import websocket
import traceback
import json
import sys
import time
import os
from bell.consts import *
from ctypes import *
import math
import bell.ui as ui
from struct import *

try:
    import thread
except ImportError:
    import _thread as thread

(MOTOR_CMD_INVALID,
 MOTOR_CMD_CONTROL,
 MOTOR_CMD_QUERY_INFO,
 MOTOR_CMD_REPORT_INSERT,
 MOTOR_CMD_REPORT_DIR_SPEED,
 MOTOR_CMD_REPORT_STOP_RUN,
 *_)  = range(100)

    
class XferHdrT(Structure):
    _fields_ = [('magic', c_uint8),
                ('crc16', c_uint16),
                ('seq', c_uint8),
                ('appid', c_uint8),
                ('channel', c_uint8, 5),
                ('phy_type', c_uint8, 3),
                ('cmd', c_uint8, 7),
                ('report', c_uint8, 1),
                ('rc', c_uint8),
                ('len', c_uint16),
                ('data', c_char_p),
                ]

def hal_handler(data, length):
    # Pointer instances have a contents attribute which returns the object to which the pointer points,
    print('recv hal data {}'.format(data))
    print('recv hal len {}'.format(length))
    print('recv hal data.contents {}'.format(data.contents))
    print('recv hal data.contents.cmd {}'.format(data.contents.cmd))
    print('recv hal data.contents.data.len {}'.format(data.contents.len))
    
lib_path = '/lib/arm-linux-gnueabihf/libtbot.so'
lib = cdll.LoadLibrary(lib_path)
REGISTER_RECVCB = CFUNCTYPE(c_void_p, c_char_p, c_uint32)
cb = REGISTER_RECVCB(hal_handler)
lib.register_recvcb(cb)
lib.tbot_lib_init()
time.sleep(15)
