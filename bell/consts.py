# coding: utf-8

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

# 外设接口
(TBOT_PORT_INVALID,
 TBOT_PORT_I2C_UART_1,
 TBOT_PORT_I2C_UART_2,
 TBOT_PORT_I2C_UART_3,
 TBOT_PORT_I2C_UART_4,
 TBOT_PORT_I2C_UART_5,
 TBOT_PORT_I2C_UART_6,
 TBOT_PORT_SERVO_1,
 TBOT_PORT_SERVO_2,
 TBOT_PORT_SERVO_3,
 TBOT_PORT_SERVO_4,
 TBOT_PORT_MOTOR_1,
 TBOT_PORT_MOTOR_2,
 TBOT_PORT_MOTOR_3,
 TBOT_PORT_MOTOR_4,
 TBOT_PORT_MOTOR_5,
 TBOT_PORT_MOTOR_6,
 TBOT_PORT_MAX, *_) = range(100)

# 电机状态
(MOTOR_OFF,
 MOTOR_FORWARD_FAST_DECAY,
 MOTOR_FORWARD_SLOW_DECAY,
 MOTOR_REVERSE_FAST_DECAY,
 MOTOR_REVERSE_SLOW_DECAY,
 *_) = range(100)


# class XferHdrT(Structure):
#     _fields_ = [("magic", c_uint8),
#                 ("crc16", c_uint16),
#                 ("seq", c_uint8),
#                 ("appid", c_uint8),
#                 ("channel", c_uint8, 5),
#                 ("phy_type", c_uint8, 3),
#                 ("cmd", c_uint8, 7),
#                 ("report", c_uint8, 1),
#                 ("rc", c_uint8),
#                 ("len", c_uint8),
#                 ("data", c_char_p),
#                 ]
