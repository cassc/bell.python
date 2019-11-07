# coding: utf-8

from bell import api
import time
            
def show_all_component():
    ctx = api.BellControl()
    try:
        ctx.init()
        ctx.display_text('hello from python', 100, 120, clear=True)
        time.sleep(3)
        ctx.display_text('goodbye', 100, 120, clear=True)
        time.sleep(2)
    finally:
        ctx.close()

show_all_component()
