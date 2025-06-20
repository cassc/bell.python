# coding: utf-8

# https://github.com/websocket-client/websocket-client
import logging
import websocket
import traceback
import json
import sys
import time
import os
from bell.consts import *
from ctypes import *
import math
import bell.ui as ui
from struct import *

try:
    import thread
except ImportError:
    import _thread as thread

WS_ADDR = 'ws://localhost:18282'

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def prepend_resource_path(filename):
    root = os.environ.get('RES_HOME')
    return os.path.join(root, filename)

def hal_handler(buf, length):
    msg = ''.join([chr(buf[i]) for i in range(length)])
    l_info('recv hal {} {}'.format(msg, length))

# def init_logging():
#     program_name = sys.argv[0]
#     logfile = '/tmp/libbel_{}.log'.format(program_name[:-3].replace('/', '.'))
    
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.INFO)
#     f_format = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
#     fhandler = logging.FileHandler(logfile, mode='w', encoding='utf8')
#     fhandler.setFormatter(f_format)
#     logger.addHandler(fhandler)
#     return logger

# logger = init_logging()

def l_info(msg, *args):
    logging.info(msg, *args)

def default_event_handler(ctx, event):
    l_info('Event received: {}'.format(event))

def on_error(ws, error):
    l_info(error)


def prepare_ui_data(data):
    return {'tpe': 'ui.update',
            'from': 'libbell',
            'target': 'ui',
            'component-data': data}

def get_file_path():
    return sys.argv[0]

def on_open(ws):
    l_info('ws opened')
    ws.send(json.dumps({'tpe': 'ui.init',
                        'from': 'libbell',
                        'target': 'ui',
                        'data': {'cmd-path': get_file_path()}}))

class BellControl():
    def __init__(self, handler=default_event_handler):
        def hfn(req):
            handler(self, req)
        self.handler = hfn
        self.lib = None
        self.ws=None
        self.ws_init()
        time.sleep(1)
            
    def __enter__(self):
        return self

    def __exit__(self,  exc_type, exc_val, exc_tb):
        self.close()

   
    def __maybe_start_ws__(self):
        if not self.ws:
            self.start_websocket()
            
    def start_websocket(self):
        websocket.enableTrace(False)

        def on_close(_):
            l_info('ws closed')
            self.ws=None

        def on_message(ws, msg):
            try:
                req = json.loads(msg)
                if ('target' in req) and ('api' in req['target']):
                    self.handler(req)
            except Exception as e:
                l_info('handle message error: {}'.format(e))
                l_info(traceback.format_exc())
                

            
        ws = websocket.WebSocketApp(self.addr,
                                    on_message = on_message,
                                    on_error = on_error,
                                    on_close = on_close,
                                    on_open = on_open)
        def run():
            l_info('ws connection starting')
            ws.run_forever()
            l_info('ws connection closed')
        self.ws = ws
        thread.start_new_thread(run, ())

    def ws_init(self):
        self.addr = WS_ADDR
        self.start_websocket()


    def init(self):
        while True:
            if self.ready():
                program_name = sys.argv[0]
                msg = 'Init success {}'.format(program_name.split('/')[-1])
                self.display_text(msg, 10, 100)
                break
            time.sleep(1)
            l_info('waiting ws')
            
    def send(self, msg):
        self.__maybe_start_ws__()
        if self.ws_ready():
            self.ws.send(msg)
            return True
        return False

    def ready(self):
        return self.ws_ready()
    
    def ws_ready(self):
        return self.ws and self.ws.sock

    
    def servo_control(self, port, angle):
        # todo
        pass
    
    def async_query_ultrasonic(self, port):
        '''从超声波感器读取距离'''
        self.send(json.dumps({'tpe': 'hal.us.read',
                              'from': 'libbell',
                              'target': 'be',
                              'data': port}))

    def async_query_color(self, port):
        '''从颜色感器读取RGB值'''
        self.send(json.dumps({'tpe': 'hal.col.read',
                              'from': 'libbell',
                              'target': 'be',
                              'data': port}))
        
        
    def async_query_sensor_line(self, port):
        # todo
        pass
    
    def async_control_coded_motor(self, port, state, period_us, duty_us):
        self.send(json.dumps({'tpe': 'hal.mot.ctrl',
                              'from': 'libbell',
                              'target': 'be',
                              'data': dict(port=port,
                                           state=state,
                                           period=period_us,
                                           duty=duty_us)}))

    
    def close(self):
        self.send_close_user_ui()
        if self.ws is not None:
            self.ws.close()

    def display_text(self, content, x, y, clear=False, max_width=SCREEN_WIDTH, color='white', font_size=12):
        data = ui.make_text(content, x, y, clear=clear, max_width=max_width, color=color, font_size=font_size)
        self.send(json.dumps(prepare_ui_data(data)))

    def display_rect(self, x, y, w, h, r=0, clear=False, fill=False, color='white'):
        data = ui.make_rect(x, y, w, h, r, clear=clear, fill=fill, color=color)
        self.send(json.dumps(prepare_ui_data(data)))

    def display_circle(self, x, y, r, clear=False, fill=False, color='white'):
        data = ui.make_circle(x, y, r, clear=clear, fill=fill, color=color)
        self.send(json.dumps(prepare_ui_data(data)))

    def display_ellipse(self, x, y, rx, ry, rotation=0, start_angle=0, end_angle=math.pi*2, clear=False, fill=False, color='white'):
        data = ui.make_ellipse(x, y, rx, ry, rotation, start_angle, end_angle, clear, fill, color)
        self.send(json.dumps(prepare_ui_data(data)))

        
    def display_line(self, x1, y1, x2, y2, clear=False, color='white'):
        data = ui.make_line(x1, y1, x2, y2, clear=clear, color=color)
        self.send(json.dumps(prepare_ui_data(data)))

    def display_path(self, path, clear=False, fill=False, color='white'):
        data = ui.make_path(path, clear=clear, fill=fill, color=color)
        self.send(json.dumps(prepare_ui_data(data)))

    def display_dot(self, x, y, clear=False, color='white'):
        data = ui.make_dot(x, y, clear=clear, color=color)
        self.send(json.dumps(prepare_ui_data(data)))

    def send_close_user_ui(self):
        params = {'tpe': 'ui.close',
                  'from': 'libbell',
                  'target': 'ui',}
        self.send(json.dumps(params))
        

    # def set_window_background(self, r, g, b, a):
    #     params = {'tpe': 'ui.update',
    #               'from': 'libbell',
    #               'target': 'ui',
    #               'component-data': {'type': 'text-msg',
    #                                  'data': {'content': msg},}}
    #     self.send(json.dumps(params))
        
    def clear_display(self, clear_rect=None):
        data = ui.make_clear(clear_rect=clear_rect)
        self.send(json.dumps(prepare_ui_data(data)))

    def show_sequence(self, xs, clear_first=False):
        if clear_first:
            xs = [{'type': 'clear', 'clear': True,}] +xs
        params = {'tpe': 'ui.update',
                  'from': 'libbell',
                  'target': 'ui',
                  'xs': xs}
        self.send(json.dumps(params))

    def display_image(self, src, x, y, w, h, clear=False):
        data = ui.make_image(src, x, y, w, h, clear=clear)
        self.send(json.dumps(prepare_ui_data(data)))
        
    def display_animation(self, src, x, y, w, h):
        data = ui.make_animation(src, x, y, w, h)
        self.send(json.dumps(prepare_ui_data(data)))


    def play_note(self, note, octave, duration_millis):
        self.send(json.dumps({'tpe': 'play.note',
                              'from': 'libbell',
                              'target': 'be',
                              'data': {'note': note,
                                       'octave': octave,
                                       'duration_millis': duration_millis}}))

    def play_freq(self, freq, duration_millis):
        self.send(json.dumps({'tpe': 'play.freq',
                              'from': 'libbell',
                              'target': 'be',
                              'data': {'freq': freq,
                                       'duration_millis': duration_millis}}))

    def play_audio(self, filename):
        file = prepend_resource_path(filename)
        if not os.path.exists(file):
            root = os.environ.get('RES_HOME')
            raise Exception('未找到文件，请将资源文件放在{}目录'.format(root))
        self.send(json.dumps({'tpe': 'play.audio',
                              'from': 'libbell',
                              'target': 'be',
                              'data': {'filename': file,}}))
    def stop_audio(self):
        self.send(json.dumps({'tpe': 'stop.audio',
                              'from': 'libbell',
                              'target': 'be',}))

    def start_recorder(self, filename):
        file = prepend_resource_path(filename)
        if os.path.exists(file):
            raise Exception('文件已存在！')
        self.send(json.dumps({'tpe': 'start.recorder',
                              'from': 'libbell',
                              'target': 'be',
                              'data': {'filename': prepend_resource_path(filename),}}))
        
    def stop_recorder(self):
        self.send(json.dumps({'tpe': 'stop.recorder',
                              'from': 'libbell',
                              'target': 'be',}))
        
