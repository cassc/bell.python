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
    
    if req['tpe'] not in ['event.keydown', 'event.longpress']:
        return

    ky = req['data']['keycode']

    longpress = req['tpe'] == 'event.longpress'

    if ky == 'down':
        y += step 
    elif ky == 'up':
        y -= step
    elif ky == 'left':
        x -= step
    elif ky == 'right':
        x += step
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
