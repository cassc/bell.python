# coding: utf-8

from bell import api
from bell import ui
from bell.consts import *
import time
import math
from random import randint


def event_handler(ctx, req):
    print('recv event: {}'.format(req))


ctx = api.BellControl(handler=event_handler)
ctx.init()
ctx.clear_display()
ctx.display_circle(160, 120, 20, fill=True, clear=True)
ctx.tbot_control_coded_motor(TBOT_PORT_MOTOR_4, MOTOR_FORWARD_FAST_DECAY, 1000, 500, 1000)
time.sleep(5)
ctx.tbot_control_coded_motor(TBOT_PORT_MOTOR_4, MOTOR_OFF, 1000, 500, 50)
time.sleep(30)


