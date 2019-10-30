#!/usr/bin/env python
# coding: utf-8

# 导入bell依赖包
from bell import api

# 用户也可导入其它标准包
import time

def test_ui_and_servo():
    # 初始化类
    b = api.BellControl()
    try:
        # 程序开始执行，默认显示程序的名称
        b.init()

        time.sleep(2)

        # 在屏幕上显示自定义文本框
        b.display_text('hello from python lib', 160, 120)

        time.sleep(2)
        print('准备测试舵机')
        b.display_text('准备测试舵机', 180, 120, clear=True)
        time.sleep(1)
        # b.servo_control(1, 50)
        time.sleep(3)
        b.display_text('结束程序', 180, 120, clear=True)
        time.sleep(3)
    finally:
        # 结束时调用
        b.close()
