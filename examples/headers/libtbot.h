/**
 * @file api_libtbot.h
 * @brief api 
 * 
 */

#define __API_LIBTBOT_H__

/**
 * @brief 设备类型
 * 
 */
typedef enum tbot_dev_type {
    TBOT_DEV_TYPE_INVALID,

    TBOT_DEV_TYPE_COLOR_SENSOR, ///< 颜色传感器
    TBOT_DEV_TYPE_servo_motor, ///< 舵机
    TBOT_DEV_TYPE_CODED_MOTOR_A, ///< 电机
    TBOT_DEV_TYPE_ultrasonic_sensor, ///< 超声波传感器
    TBOT_DEV_TYPE_line_following_SENSOR, ///< 巡线传感器

} tbot_dev_type_t;

/**
 * @brief tbot设备端口
 * 
 */
typedef enum {
    TBOT_PORT_INVALID = 0,

    TBOT_PORT_I2C_UART_1, ///< I2C/UART端口1
    TBOT_PORT_I2C_UART_2, ///< I2C/UART端口2
    TBOT_PORT_I2C_UART_3, ///< I2C/UART端口3
    TBOT_PORT_I2C_UART_4, ///< I2C/UART端口4
    TBOT_PORT_I2C_UART_5, ///< I2C/UART端口5
    TBOT_PORT_I2C_UART_6, ///< I2C/UART端口6

    TBOT_PORT_SERVO_1, ///< 舵机端口1
    TBOT_PORT_SERVO_2, ///< 舵机端口2
    TBOT_PORT_SERVO_3, ///< 舵机端口3
    TBOT_PORT_SERVO_4, ///< 舵机端口4

    TBOT_PORT_MOTOR_1, ///< 电机端口1
    TBOT_PORT_MOTOR_2, ///< 电机端口2
    TBOT_PORT_MOTOR_3, ///< 电机端口3 
    TBOT_PORT_MOTOR_4, ///< 电机端口4
    TBOT_PORT_MOTOR_5, ///< 电机端口5
    TBOT_PORT_MOTOR_6, ///< 电机端口6

    TBOT_PORT_MAX
} tbot_port_t;


typedef struct {
    tbot_port_t port;
    uint8_t  is_forward;
    uint32_t speed;
} motor_info_t;

/**
 * @brief 电机控制
 * 
 */
enum motor_state {
    MOTOR_OFF, ///< 电机停止
    MOTOR_FORWARD_FAST_DECAY, ///< 电机正转急停
    MOTOR_FORWARD_SLOW_DECAY, ///< 电机正转慢停
    MOTOR_REVERSE_FAST_DECAY, ///< 电机反转急停
    MOTOR_REVERSE_SLOW_DECAY, ///< 电机反转慢停
};

/**
 * @brief 电机控制参数
 * 
 */
typedef struct motor_ctrl {
    tbot_port_t port;
    enum motor_state state;  
    uint32_t period_us; 
    uint32_t duty_us; 
    uint32_t need_pulse; 
}  __attribute__ ((packed)) motor_ctrl_t;  

/**
 * @brief 系统上报事件回调函数
 * 
 */
typedef void (*recv_cb_t)(uint8_t *data, uint32_t len);

/**
 * @brief 主控RK向协处理器发送指令，并等待协处理器返回
 * 
 * 该指令为请求应答机制，RK向ST发送指令， ST执行后返回，如果ST未在超时时间内响应，
 * 函数执行失败。
 * 
 * @param channel 通信通道
 * @param cmd  具体命令
 * @param tx 主控输入指令
 * @param txlen 主控输入指令长度
 * @param rx 协处理器返回的数据， 该设置为NULL
 * @param rx_inout_len 协处理器返回的数据长度，可设置为NULL
 * @param err 可以传NULL值，如果不为空，且指令执行出错，可通过该变量获取失败原因。
 * @param timeout_ms 超时时间，单位毫秒
 * @return int 返回0，指令执行成功，否则失败，失败时可通过读取err值获取失败原因。 
 */
int tbot_send_app_msg(
            xfer_channel_t channel, uint8_t cmd,  
            void *tx, uint32_t txlen, 
            void *rx, uint32_t *rx_inout_len,
            int *err, uint32_t timeout_ms);

/**
 * @brief 注册系统回调事件
 * 
 * @param recv_cb 回调事件处理函数
 */
void register_recvcb(recv_cb_t recv_cb);

/**
 * @brief 不再接收系统上报事件。
 * 
 */
void unregister_recvcb(void);

/**
 * @brief 初始化libso库，失败应该不再执行接下来的逻辑。
 * 
 * @return int 返回-：成功，否则失败。
 */
int tbot_lib_init(void);

/** 
 * 进程退出时执行，释放libso占用的系统资源
 */
void tbot_lib_exit(void);

/**
 * 打开so库调式信息
 * 
 */
void tbot_debug_on(void);

/**
 * 关闭so库调式信息
 * 
 */
void tbot_debug_off(void);

/**
 * @brief 启动指定端口自动查询功能
 * 
 * @param port 
 * @return int 
 */
int tbot_auto_query_start(tbot_port_t port);

/**
 * @brief 启动指定端口自动查询功能
 * 
 * @param port 
 * @return int 
 */
int tbot_auto_query_stop(tbot_port_t port);

/**
 * @brief 获取指定端口的设备类型
 * 
 * @param port 
 * @param device_type 
 * @return int 
 */
int tbot_query_devtype(tbot_port_t port, tbot_dev_type_t *device_type);

/**
 * @brief 巡线传感器数据获取
 * 
 * @param port 要采集的端口
 * @param rxbuf 获取的数据，第一字节为左侧采集数据，第二字节为右侧采集数据。
 * @param len 长度 >= 2
 * @return int 0: 成功，否则失败。
 */
int tbot_query_sensor_line_following(
        tbot_port_t port, uint8_t *rxbuf, uint8_t len);


/**
 * @brief 颜色传感器
 * 
 * @param port 要采集的端口
 * @param rxbuf 获取的数据，3字节， 第一到第三字节分别为r,g,b颜色数据
 * @param len 输入必须满足 >= 3
 * @return int 0: 成功，否则失败。
 */
int tbot_query_color_sensor(
        tbot_port_t port, uint8_t *rxbuf, uint8_t len);

/**
 * @brief 超声波传感器
 * 
 * @param port 要采集的端口
 * @param rxbuf 获取的超声波距离数据，单位毫米
 * @return int 0: 成功，否则失败。
 */
int tbot_query_ultrasonic_sensor(
        tbot_port_t port, uint32_t *rxbuf);


/**
 * @brief 舵机传感器
 * 
 * @param port 要控制的端口
 * @param angle 转动角度，取值 0 到 180度 
 * @return int 0: 成功，否则失败。
 */
int tbot_control_servo_motor(
        tbot_port_t port, uint32_t angle);


/**
 * @brief 
 * 
 * @param port 
 * @param state 
 * @param period_us 周期：单位微秒
 * @param duty_us 占空比，高电平持续时间：单位微秒
 * @param timeout_ms  指令超时时间
 * @return int 
 */
int tbot_control_coded_motor(
        tbot_port_t port, enum motor_state state, 
        uint32_t period_us, uint32_t duty_us, uint32_t timeout_ms);


#endif
