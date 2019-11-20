# coding: utf-8


from bell import api
from bell import ui

try:
    import thread
except ImportError:
    import _thread as thread

import time
import serial
import json
import base64
import re

port = '/dev/ttyUSB0'
ser = serial.Serial(
    port=port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

if not ser.isOpen():
    print('Open serial port {} fail'.format(port))

print('Open serial port success')

points = [0 for _ in range(0, 320)]


def run_serail_data_fetcher():
    global points
    while True:
        ser.write('GTEMP'.encode('ascii'))
        ser.flush()
        print('write success')
        time.sleep(0.1)
        while ser.inWaiting() > 0:
            ss= ser.read(2)
            rs = int.from_bytes(ss, byteorder='big')
            print('recv: {}'.format(rs))
            points.append(rs)
            while len(points) > 320:
                points.pop(0)
    
def draw_curve(ctx):
    pth = [[i, (240 - (points[i]/1024.0) * 240)] for i in range(0, 320)]
    cx = [ui.make_path(pth),
          ui.make_text('val {}'.format(points[-1]), 10, 10)]
    ctx.show_sequence(cx, clear_first=True)

def start_draw():
    ctx = api.BellControl()
    try:
        ctx.init()
        ctx.clear_display()
        while True:
            draw_curve(ctx)
            time.sleep(0.1)
    finally:
        ctx.close()
    
def start():
    thread.start_new_thread(run_serail_data_fetcher, ())
    start_draw()

start()
