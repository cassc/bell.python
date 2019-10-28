#!/usr/bin/env python
# coding: utf-8

# 导入bell依赖包
from libbell import bell as b

# 用户也可导入其它标准包
import time

# 初始化类
b = b.BellControl()
try:
    # 程序开始执行，默认显示程序的名称
    b.init()

    time.sleep(2)

    # 在屏幕上显示自定义文本框
    # b.display_text_box('hello from python lib')

    time.sleep(2)
    print('准备测试舵机')
    b.display_text_box('准备测试舵机')
    time.sleep(1)
    # b.servo_control(1, 50)
    time.sleep(3)
    b.display_text_box('结束程序')
    time.sleep(3)
finally:
    # 结束时调用
    b.close()
