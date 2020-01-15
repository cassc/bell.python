# coding: utf-8

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


(GPIO_CMD_INVALID,
 GPIO_CMD_OUT_HIGH,
 GPIO_CMD_OUT_LOW,
 GPIO_CMD_IN_PULLUP,
 GPIO_CMD_IN_PULLDOWN,
 GPIO_CMD_IN_NOPULL,*_) = range(100)

(ADC_CMD_INVALID,
 ADC_CMD_GET_ADC,
 ADC_CMD_GPIO_OUT_HIGH,
 ADC_CMD_GPIO_OUT_LOW,
 ADC_CMD_GPIO_IN_PULLUP,
 ADC_CMD_GPIO_IN_PULLDOWN,
 ADC_CMD_GPIO_IN_NOPULL,*_) = range(100)

# 外设接口
(TBOT_PORT_INVALID,
 TBOT_PORT_I2C_UART_1,
 TBOT_PORT_I2C_UART_2,
 TBOT_PORT_I2C_UART_3,
 TBOT_PORT_I2C_UART_4,
 TBOT_PORT_I2C_UART_5,
 TBOT_PORT_I2C_UART_6,
 TBOT_PORT_MOTOR_1,
 TBOT_PORT_MOTOR_2,
 TBOT_PORT_MOTOR_3,
 TBOT_PORT_MOTOR_4,
 TBOT_PORT_MOTOR_5,
 TBOT_PORT_MOTOR_6,
 TBOT_PORT_PWM_1,
 TBOT_PORT_PWM_2,
 TBOT_PORT_PWM_3,
 TBOT_PORT_PWM_4,
 TBOT_PORT_ADC_1,
 TBOT_PORT_ADC_2,
 TBOT_PORT_ADC_3,
 TBOT_PORT_ADC_4,
 TBOT_PORT_GPIO_1,
 TBOT_PORT_GPIO_2,
 TBOT_PORT_GPIO_3,
 TBOT_PORT_GPIO_4,
 TBOT_PORT_MAX,
 *_) = range(100)
    
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
    data = data[0:length]
    edata = json.loads(data)
    print('get data: {}'.format(edata))
    
    
lib_path = '/lib/arm-linux-gnueabihf/libtbot.so'
lib = cdll.LoadLibrary(lib_path)
REGISTER_RECVCB = CFUNCTYPE(c_void_p, c_char_p, c_uint32)
cb = REGISTER_RECVCB(hal_handler)
lib.register_recvcb(cb)
lib.tbot_lib_init()

time.sleep(2)
# int tbot_adc_control(tbot_port_t port,  enum adc_cmd cmd, uint32_t *adc_mv, uint32_t timeout_ms);
val = c_uint32()
lib.tbot_adc_control(TBOT_PORT_ADC_1, ADC_CMD_GET_ADC, byref(val), c_uint32(3000))
print('adc val {}'.format(val.value))

pin_val = c_uint8()
# int tbot_gpio_control(tbot_port_t port,  enum gpio_cmd cmd, uint8_t *gpio_in_val, uint32_t timeout_ms);
lib.tbot_gpio_control(TBOT_PORT_GPIO_1, GPIO_CMD_OUT_LOW, byref(pin_val), c_uint32(3000));
print('pin val {}'.format(pin_val.value))
time.sleep(2)
lib.tbot_gpio_control(TBOT_PORT_GPIO_1, GPIO_CMD_OUT_HIGH, byref(pin_val), c_uint32(3000));
print('pin val {}'.format(pin_val.value))

time.sleep(15)
