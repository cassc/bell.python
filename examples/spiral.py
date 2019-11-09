# coding: utf-8

from bell import api
import time
import math


offset = (180, 120)
pth = [offset]
# http://mathworld.wolfram.com/LogarithmicSpiral.html

def gen_spirals():
    a = 1
    b = 0.2
    theta = 0
    degree = math.pi/180
    while True:
        pw = math.e ** (b*theta)
        x = a * math.cos(theta) * pw
        y = a * math.sin(theta) * pw
        yield (x, y)
        theta += 2 * degree

def update_xy(gen):
    (x, y) = next(gen)
    pth.append((offset[0]+x, offset[1] +y))
    while len(pth) > 20:
        pth.pop(0)

def draw_curve(ctx, gen):
    update_xy(gen)
    ctx.display_path(pth)

def start():
    ctx = api.BellControl()
    try:
        ctx.init()
        time.sleep(0.2)
        ctx.clear_display()
        gen = gen_spirals()
        update_xy(gen)
        update_xy(gen)
        while True:
            draw_curve(ctx,gen)
            time.sleep(0.01)
            if pth[-1] > tuple(i*2 for i in offset):
                break
    finally:
        ctx.close()

start()
