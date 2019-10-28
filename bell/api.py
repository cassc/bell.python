# coding: utf-8

# https://github.com/websocket-client/websocket-client
import websocket
import json
import sys
import time
import os
from ctypes import *

try:
    import thread
except ImportError:
    import _thread as thread


SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
WS_ADDR = 'ws://127.0.0.1:18282'

def on_message(ws, message):
    print('recv {}'.format(message))

def on_error(ws, error):
    print(error)


def on_open(ws):
    print('ws opened')

class BellControl():
    def maybe_start_ws(self):
        if not self.ws:
            self.start_websocket()
    
    def start_websocket(self):
        websocket.enableTrace(True)

        def on_close(ws):
            print('ws closed')
            self.ws=None
        
        ws = websocket.WebSocketApp(self.addr,
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close,
                                    on_open = on_open)
        def run():
            print('ws connection starting')
            ws.run_forever()
            print('ws connection closed')
        self.ws = ws
        thread.start_new_thread(run, ())

    def ws_init(self):
        self.addr = WS_ADDR
        self.start_websocket()

    def lib_init(self):
        lib = None
        lib_path = os.environ.get('LIBC_PATH')
        if lib_path is None:
            lib_path = '/home/firefly/tbot/spi/tbot_lib/lib/libtbot.so'
        print('Load c lib from {}'.format(lib_path))
        lib = cdll.LoadLibrary(lib_path)

        if lib is not None and self.handler is not None:
            # void register_recvcb(void (*recv_cb)(void *data, uint32_t len));
            REGISTER_RECVCB = CFUNCTYPE(c_void_p, c_char_p, c_uint)
            cb = REGISTER_RECVCB(self.handler)
            # int tbot_lib_init(void);
            lib.register_recvcb(cb)
        self.lib = lib
        ret = -1 if lib is None else lib.tbot_lib_init()
        success = lib is not None and ret == 0
        print('Initialize lib {}, init ret {}'.format('success' if success else 'failed', ret))
        return success

        
    def __init__(self, handler=None):
        self.handler = handler
        self.lib = None
        self.ws_init()
        # self.lib_init()
        

    def init(self):
        while True:
            if self.ready():
                program_name = sys.argv[0]
                msg = 'Executing {}'.format(program_name)
                self.display_text(msg, 120, 120)
                break
            time.sleep(1)
        
    def send(self, msg):
        self.maybe_start_ws()
        if self.ws_ready():
            self.ws.send(msg)
            return True
        return False

    def ready(self):
        return self.ws_ready()
            
    def ws_ready(self):
        return self.ws and self.ws.sock

    def get_lib(self):
        if self.lib is None:
            raise Exception('Library not loaded')
        return self.lib
    
    def servo_control(self, port, angle):
        lib = self.get_lib()
        return lib.tbot_control_servo_motor(port, angle)
        

    def query_sensor_line(self, port):
        lib = self.get_lib()
        data_len = 2
        data_out = create_string_buffer(data_len)
        ret = lib.tbot_query_sensor_line_following(port, data_out, data_len)
        
        if not ret:
            return repr(data_out.raw)
        print('查询巡线传感器状态失败，ret {}' % ret)
        return None

    def close(self):
        self.send_close_user_ui()
        if self.ws is not None:
            self.ws.close()

    def display_text(self, content, x, y, clear=False, max_width=SCREEN_WIDTH, color='black', font_size=12):
        params = {'tpe': 'ui.update',
                  'from': 'libbell',
                  'target': 'ui',
                  'component-data': {'type': 'text-msg',
                                     'clear': clear,
                                     'data': {'content': content,
                                              'x': x,
                                              'y': y,
                                              'max-width': max_width,
                                              'color': color,
                                              'font-size': font_size,
                                     },}}
        self.send(json.dumps(params))

    def display_rect(self, x, y, w, h, clear=False, fill=False, color='black'):
        params = {'tpe': 'ui.update',
                  'from': 'libbell',
                  'target': 'ui',
                  'component-data': {'type': 'rect',
                                     'clear': clear,
                                     'data': {'x': x,
                                              'y': y,
                                              'w': w,
                                              'h': h,
                                              'fill': fill,
                                              'color': color,
                                     },}}
        self.send(json.dumps(params))

    def display_circle(self, x, y, r, clear=False, fill=False, color='black'):
        params = {'tpe': 'ui.update',
                  'from': 'libbell',
                  'target': 'ui',
                  'component-data': {'type': 'circle',
                                     'clear': clear,
                                     'data': {'x': x,
                                              'y': y,
                                              'r': r,
                                              'fill': fill,
                                              'color': color,
                                     },}}
        self.send(json.dumps(params))

    def display_line(self, x1, y1, x2, y2, clear=False, color='black'):
        params = {'tpe': 'ui.update',
                  'from': 'libbell',
                  'target': 'ui',
                  'component-data': {'type': 'circle',
                                     'clear': clear,
                                     'data': {'x1': x1,
                                              'y1': y1,
                                              'x2': x2,
                                              'y2': y2,
                                              'color': color,
                                     },}}
        self.send(json.dumps(params))

    def display_path(self, path, clear=False, fill=False, color='black'):
        params = {'tpe': 'ui.update',
                  'from': 'libbell',
                  'target': 'ui',
                  'component-data': {'type': 'path',
                                     'clear': clear,
                                     'data': {'path': path,
                                              'fill': fill,
                                              'color': color,
                                     },}}
        self.send(json.dumps(params))

    def display_dot(self, x, y, clear=False, color='black'):
        params = {'tpe': 'ui.update',
                  'from': 'libbell',
                  'target': 'ui',
                  'component-data': {'type': 'dot',
                                     'clear': clear,
                                     'data': {'x': x,
                                              'y': y,
                                              'color': color,
                                     },}}
        self.send(json.dumps(params))

        
    def send_close_user_ui(self):
        params = {'tpe': 'ui.close',
                  'from': 'libbell',
                  'target': 'ui',}
        self.send(json.dumps(params))
        

    def set_window_background(self, r, g, b, a):
        params = {'tpe': 'ui.update',
                  'from': 'libbell',
                  'target': 'ui',
                  'component-data': {'type': 'text-msg',
                                     'data': {'content': msg},}}
        self.send(json.dumps(params))
        
