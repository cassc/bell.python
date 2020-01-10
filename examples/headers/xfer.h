/**
 * @file app_xfer.h
 * @brief 
 * 
 */

#define __APP_XFER_H__

#define XFER_MAGIC 0x7E

#define TBOT_SPI_DMA_LEN 128

#define XFER_MAX_PACKET_LEN (1024)
#define XFER_MAX_DATA_LEN (XFER_MAX_PACKET_LEN - sizeof(xfer_hdr_t))

typedef enum {
    XFER_PHY_TYPE_BT = 0,
    XFER_PHY_TYPE_USB = 1,
    XFER_PHY_TYPE_WIFI = 2,
} xfer_phy_type_t;

typedef enum {
    XFER_NOT_REPORT = 0,
    XFER_REPORT = 1,
} xfer_report_t;

typedef enum {
    XFER_SUCCESS = 0,

    XFER_ERR_UNKNOWN,
    XFER_ERR_CHANNEL,
    XFER_ERR_CMD,
    XFER_ERR_SYSTEM,
} xfer_err_t;

typedef enum {
    SYS_CMD_INVALID = 0,
    SYS_CMD_QUERY_ENABLE,
    SYS_CMD_QUERY_DISABLE,
    SYS_CMD_QUERY_PORT,
    SYS_CMD_CONTROL_SERVO_MOTOR,
} sys_cmd_t;


enum motor_cmd {
    MOTOR_CMD_INVALID = 0,
    MOTOR_CMD_CONTROL,
    MOTOR_CMD_QUERY_INFO,

    MOTOR_CMD_REPORT_INSERT,
    MOTOR_CMD_REPORT_DIR_SPEED,
    MOTOR_CMD_REPORT_STOP_RUN,
};

/**
 * @brief 通信通道
 * 
 */
typedef enum {
    XFER_CHANNEL_INVALID = 0,
    XFER_CHANNEL_SYSTEM,	///< 系统通道
    XFER_CHANNEL_MOTOR, //encoder
} xfer_channel_t;


typedef struct {
    uint8_t magic;
    uint16_t crc16;
    //
    uint8_t seq;
    uint8_t appid;

    //
    uint8_t channel: 5;
    uint8_t phy_type: 3; // xfer_phy_type_t
    
    uint8_t cmd: 7;
    uint8_t report: 1;
    
    uint8_t  rc;
    
    uint16_t len;
    uint8_t data[0];
}  __attribute__ ((packed)) xfer_hdr_t;

typedef struct {
    uint8_t len;
    uint8_t data[0];
}  __attribute__ ((packed)) split_hdr_t;


static inline uint16_t xfer_packet_len(xfer_hdr_t *p_xfer)
{
    return sizeof(xfer_hdr_t) + p_xfer->len;
}

static inline uint16_t xfer_data_len(xfer_hdr_t *p_xfer)
{
    return p_xfer->len;
}

int pack_xfer_msg(void *outbuf, uint16_t outbuf_len,
            uint8_t app_id, xfer_phy_type_t phy_type, 
            xfer_channel_t channel, uint8_t msgcmd,  
            xfer_report_t is_report, uint8_t rc, void *data, uint16_t datalen);

int is_xfer_msg_valid(void *packet, uint32_t len);
void change_xfer_msg_appid(xfer_hdr_t *p_xfer, int new_appid);

int send_app_msg_raw(int cfd, uint8_t app_id, xfer_phy_type_t phy_type, 
            xfer_channel_t channel, uint8_t msgcmd,  
            xfer_report_t is_report, uint8_t rc, void *data, uint16_t datalen);

int response_app_msg(int cfd, xfer_hdr_t *p_rxhdr, 
        uint8_t rc, void *pdata, uint16_t datalen);

#endif
