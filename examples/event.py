# coding: utf-8

from bell import api
from bell import ui
import time
import math
from random import randint


x = 180
y = 120
r = 20
step = 8

def event_handler(ctx, req):
    global x
    global y
    global r
    global step 
    if req['tpe'] != 'event.keydown':
        return
    ky = req['data']['keycode']
    if ky == 'down':
        y += 1
    elif ky == 'up':
        y -= 1
    elif ky == 'left':
        x -= 1
    elif ky == 'right':
        x += 1
    txt = ui.make_text(str(req), 20, 20)
    ball = ui.make_circle(x, y, r, fill=True)
    ctx.show_sequence([txt, ball], clear_first=True)

def start():
    global x
    global y
    global r
    ctx = api.BellControl(handler=event_handler)
    ctx.init()
    ctx.clear_display()
    ctx.display_circle(x, y, r, fill=True, clear=True)
    time.sleep(60000)
    
start()
