# coding: utf-8

from bell import api
from bell import ui
import time
import math
from random import randint


x = 180
y = 120

p_title = (10, 40)
i = 0

star_path = [[x, y],
             [x+20, y+100],
             [x, y+80],
             [x-20, y+100],
]

xs = [[ui.make_text('图片', *p_title),
       ui.make_image('anim.gif', 10, 40, 120, 120)],
      [ui.make_text('文字', *p_title),
       ui.make_text('文本', 150, 120, font_size=24, color='cyan'),],
      [ui.make_text('GIF动画', *p_title),
       ui.make_animation('anim.gif', 0, 0, 320, 240)],
      [ui.make_text('圆', *p_title),
       ui.make_circle(x, y, 10, fill=True)],
      [ui.make_text('多边形', *p_title),
       ui.make_path(star_path, fill=True)],
      [ui.make_text('椭圆', *p_title),
       ui.make_ellipse(x, y, 60, 40, 0, 0, math.pi, fill=True),
       ui.make_ellipse(x, y, 60, 40, 0, math.pi, math.pi*2, fill=False)],
      [ui.make_text('方形', *p_title),
       ui.make_rect(x, y, 40, 40, 4, fill=True),
       ui.make_rect(x+40, y, 40, 40),
       ui.make_rect(x, y+40, 40, 40),
       ui.make_rect(x+40, y+40, 40, 40, 4, fill=True),]
      ,
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
