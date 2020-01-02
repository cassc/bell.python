# coding: utf-8

from bell import api
from bell import ui
import time
import math
from random import randint, choice


offset = (180, 120)
xy = [0 for _ in range(0, 320)]

def update_xy():
    xy.append(randint(0, 240))
    if len(xy) > 320:
        xy.pop(0)

def draw_curve(ctx):
    update_xy()
    pth = [[i, 240-xy[i]] for i in range(0, 320)]
    ctx.display_path(pth, clear = True)

            
def start():
    ctx = api.BellControl()
    try:
        ctx.init()
        ctx.clear_display()
        while True:
            draw_curve(ctx)
            time.sleep(0.05)
    finally:
        ctx.close()

start()
