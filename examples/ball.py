# coding: utf-8

from bell import api
from bell import ui
import time



offset = (180, 120)

def make_face():
    (x, y, r) = (240, 60, 40)
    ileft = (x - 15, y-15, 10)
    iright = (x + 15, y-15, 10)
    mouth = (x, y+20, 10, 5)
    a = ui.make_circle(x, y, r, clear=False)
    il = ui.make_circle(*ileft, color='red', fill=True, clear=False)
    ir = ui.make_circle(*iright, color='red', fill=True, clear=False)
    m =ui.make_ellipse(*mouth, color='green', fill=True, clear=False)
    box = ui.make_rect(x-45, y-45, 90, 90, 10)
    return [a, il, ir, m, box]
    

def draw_bouncing_ball(ctx):
    x, y, r = (10, 10, 10)
    ctx.display_circle(x, y, r, fill=True,clear=True)
    down = True
    u = 10
    sleep = 0.01
    face = make_face()
    balls = []

    def append_shadows(sq, down):
        for i in range(1, 10, 2):
            y_offset = -1 if down else 1
            y_offset *= i
            sq.append(ui.make_circle(x, y + y_offset, r, fill=True, color='rgba(0,0,0,{})'.format(1-0.1*i),  clear=False))
    
    def add_ball(x, y, r, down):
        ball = ui.make_circle(x, y, r, fill=True, clear=False)
        balls.append(ball)
        # append_shadows(sq, down)
        # ctx.show_sequence(sq, clear_first=True)

    while x< 340:
        if down:
            y = u
            while y < 230:
                balls.append((x, y, r))
                x += 0.01
                y += (y/23+0.1)
            down = False
            u = u+10
            if u > 230:
                break
        else:
            y = 230
            while y >u:
                balls.append((x, y, r))
                x += 0.05
                y -= (y/23+0.1)
            down = True
    for ball in balls:
        sq = list(face)
        sq.append(ui.make_circle(*ball, fill=True))
        ctx.show_sequence(sq, clear_first=True)
        time.sleep((250-y) /500.0)
        
def start():
    ctx = api.BellControl()
    try:
        ctx.init()
        time.sleep(0.2)
        ctx.clear_display()
        draw_bouncing_ball(ctx)
    finally:
        ctx.close()

start()
