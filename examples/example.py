# coding: utf-8

import time
import logging
from bell import api
from bell import ui


def start():
    with api.BellControl() as ctx:
        logging.info('example started')
        ctx.init()
        ctx.clear_display()
        ctx.display_text('此程序由文件目录编译/复制为程序', 10, 50)
        ctx.display_text('Python脚本直接复制', 10, 70)
        ctx.display_text('C/C++经GCC编译后再复制为可执行文件并执行', 10, 90)
        time.sleep(6)
        logging.info('example ending')
    
start()

