# coding: utf-8

from bell import api
from bell import ui
import time
import math
from random import randint


x = 180
y = 120

p_title = (10, 10)
i = 0

xs = [[ui.make_text('图片', *p_title),
       ui.make_image('cat.jpg', 10, 40, 120, 120)],
      [ui.make_text('圆', *p_title),
       ui.make_circle(x, y, 10, fill=True)],
      
]
    


def event_handler(ctx, req):
    global i
    ni = i
    if 'tpe' in req and req['tpe']=='event.keydown':
        keycode = req['data']['keycode']
        if keycode == 'left':
            if i>0:
                ni = i - 1
        if keycode == 'right':
            if i< len(xs) -1:
                ni = i + 1
    if ni != i:
        i = ni
        ctx.show_sequence(xs[i], clear_first=True)

def start():
    ctx = api.BellControl(handler=event_handler)
    ctx.init()
    ctx.show_sequence(xs[0], clear_first=True)
    time.sleep(60000)
    
start()
