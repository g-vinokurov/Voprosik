#include <stdio.h>
#include <math.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "driver/i2c.h"

#include "esp_log.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "nvs_flash.h"
#include "esp_http_server.h"

// =====================================================
// WIFI
// =====================================================

#define WIFI_SSID      "SPIDER_ROBOT"
#define WIFI_PASS      "12345678"
#define MAX_STA_CONN   4

// =====================================================
// I2C
// =====================================================

#define I2C_MASTER_SCL_IO           5
#define I2C_MASTER_SDA_IO           4
#define I2C_MASTER_NUM              I2C_NUM_0
#define I2C_MASTER_FREQ_HZ          100000

// =====================================================
// PCA9685
// =====================================================

#define PCA9685_ADDR                0x40

#define MODE1                       0x00
#define PRESCALE                    0xFE
#define LED0_ON_L                   0x06

#define SERVO_MIN                   102
#define SERVO_MAX                   410

static const char *TAG = "SPIDER";

// =====================================================
// SERVOS
// =====================================================

#define FORWARD_RIGHT_TIBIA 0
#define FORWARD_RIGHT_FEMUR 4
#define FORWARD_RIGHT_COXA 8

#define BACKWARD_RIGHT_TIBIA 1
#define BACKWARD_RIGHT_FEMUR 5
#define BACKWARD_RIGHT_COXA 9

#define BACKWARD_LEFT_TIBIA 2
#define BACKWARD_LEFT_FEMUR 6
#define BACKWARD_LEFT_COXA 10

#define FORWARD_LEFT_TIBIA 3
#define FORWARD_LEFT_FEMUR 7
#define FORWARD_LEFT_COXA 11

// =====================================================
// MODES
// =====================================================

typedef enum {
    MODE_INIT,
    MODE_MOVE,
    MODE_GO_TO_MAMA,
    MODE_TEST,
    MODE_DANCE,
    MODE_PREPARE_TO_SLEEP,
    MODE_SLEEPING,
    MODE_WAKE_UP,
    MODE_BOX
} robot_mode_t;

volatile robot_mode_t current_mode = MODE_INIT;

// =====================================================
// I2C
// =====================================================

esp_err_t i2c_master_init(void)
{
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = I2C_MASTER_FREQ_HZ,
    };
    ESP_ERROR_CHECK(i2c_param_config(I2C_MASTER_NUM, &conf));
    return i2c_driver_install(I2C_MASTER_NUM, conf.mode, 0, 0, 0);
}

// =====================================================
// PCA9685
// =====================================================

esp_err_t pca9685_write(uint8_t reg, uint8_t data)
{
    uint8_t write_buf[2] = {reg, data};

    return i2c_master_write_to_device(
        I2C_MASTER_NUM,
        PCA9685_ADDR,
        write_buf,
        sizeof(write_buf),
        pdMS_TO_TICKS(100)
    );
}

esp_err_t pca9685_set_pwm(uint8_t channel, uint16_t on, uint16_t off)
{
    uint8_t reg = LED0_ON_L + 4 * channel;

    uint8_t data[5];

    data[0] = reg;
    data[1] = on & 0xFF;
    data[2] = on >> 8;
    data[3] = off & 0xFF;
    data[4] = off >> 8;

    return i2c_master_write_to_device(
        I2C_MASTER_NUM,
        PCA9685_ADDR,
        data,
        sizeof(data),
        pdMS_TO_TICKS(100)
    );
}

void pca9685_init()
{
    pca9685_write(MODE1, 0x10);

    float freq = 50.0;

    uint8_t prescale_val =
        (uint8_t)(round(25000000.0 / (4096.0 * freq)) - 1);

    pca9685_write(PRESCALE, prescale_val);

    pca9685_write(MODE1, 0x20);

    vTaskDelay(pdMS_TO_TICKS(10));

    for (int i = 0; i < 16; i++) {
        pca9685_set_pwm(i, 0, 0);
    }

    ESP_LOGI(TAG, "PCA9685 initialized");
}

// =====================================================
// SERVO
// =====================================================

uint16_t angle_to_pwm(int angle)
{
    if (angle < 0) angle = 0;
    if (angle > 180) angle = 180;

    return SERVO_MIN +
           ((SERVO_MAX - SERVO_MIN) * angle) / 180;
}

void set_servo(uint8_t channel, int angle)
{
    uint16_t pwm = angle_to_pwm(angle);

    pca9685_set_pwm(channel, 0, pwm);

    ESP_LOGI(TAG,
             "CH %d -> angle %d",
             channel,
             angle);
}

void smooth_servo(uint8_t ch, int from, int to, int step_delay)
{
    if (from < to) {
        for (int a = from; a <= to; a += 2) {
            set_servo(ch, a);
            vTaskDelay(pdMS_TO_TICKS(step_delay));
        }
    } else {
        for (int a = from; a >= to; a -= 2) {
            set_servo(ch, a);
            vTaskDelay(pdMS_TO_TICKS(step_delay));
        }
    }
}

// =====================================================
// STAY POSITION
// =====================================================

void robot_stay_position()
{
    set_servo(FORWARD_RIGHT_COXA, 105);
    set_servo(BACKWARD_RIGHT_COXA, 60);
    set_servo(BACKWARD_LEFT_COXA, 105);
    set_servo(FORWARD_LEFT_COXA, 60);

    set_servo(FORWARD_RIGHT_FEMUR, 90);
    set_servo(BACKWARD_RIGHT_FEMUR, 90);
    set_servo(BACKWARD_LEFT_FEMUR, 90);
    set_servo(FORWARD_LEFT_FEMUR, 90);

    set_servo(FORWARD_RIGHT_TIBIA, 90);
    set_servo(BACKWARD_RIGHT_TIBIA, 90);
    set_servo(BACKWARD_LEFT_TIBIA, 90);
    set_servo(FORWARD_LEFT_TIBIA, 90);

    ESP_LOGI(TAG, "Robot stay position");
}

// =====================================================
// MOVE STEP
// =====================================================

void robot_move_cycle()
{
    smooth_servo(FORWARD_RIGHT_TIBIA, 90, 35, 10);
    smooth_servo(FORWARD_RIGHT_COXA, 105, 145, 10);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_LEFT_TIBIA, 90, 145, 10);
    smooth_servo(FORWARD_LEFT_COXA, 60, 20, 10);
    vTaskDelay(pdMS_TO_TICKS(200));
    

    smooth_servo(BACKWARD_RIGHT_TIBIA, 90, 35, 12);
    smooth_servo(BACKWARD_RIGHT_COXA, 60, 130, 12);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(BACKWARD_RIGHT_TIBIA, 35, 90, 12);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(BACKWARD_LEFT_TIBIA, 90, 145, 12);
    smooth_servo(BACKWARD_LEFT_COXA, 105, 35, 12);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(BACKWARD_LEFT_TIBIA, 145, 90, 12);
    vTaskDelay(pdMS_TO_TICKS(200));

    smooth_servo(FORWARD_LEFT_FEMUR, 90, 165, 10);
    smooth_servo(FORWARD_LEFT_TIBIA, 145, 90, 10);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(FORWARD_LEFT_FEMUR, 165, 90, 10);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_FEMUR, 90, 15, 10);
    smooth_servo(FORWARD_RIGHT_TIBIA, 35, 90, 10);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(FORWARD_RIGHT_FEMUR, 15, 90, 10);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_COXA, 145, 105, 12);
    smooth_servo(FORWARD_LEFT_COXA, 20, 60, 12);
    smooth_servo(BACKWARD_LEFT_COXA, 35, 105, 12);
    smooth_servo(BACKWARD_RIGHT_COXA, 130, 60, 12);
}

// =====================================================
// FAST MOVE STEP
// =====================================================

void robot_fast_move_cycle()
{
    smooth_servo(FORWARD_RIGHT_TIBIA, 90, 35, 5);
    smooth_servo(FORWARD_RIGHT_COXA, 105, 145, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_LEFT_TIBIA, 90, 145, 5);
    smooth_servo(FORWARD_LEFT_COXA, 60, 20, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(BACKWARD_RIGHT_TIBIA, 90, 35, 5);
    smooth_servo(BACKWARD_RIGHT_COXA, 60, 130, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(BACKWARD_RIGHT_TIBIA, 35, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(BACKWARD_LEFT_TIBIA, 90, 145, 5);
    smooth_servo(BACKWARD_LEFT_COXA, 105, 35, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(BACKWARD_LEFT_TIBIA, 145, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_LEFT_FEMUR, 90, 165, 5);
    smooth_servo(FORWARD_LEFT_TIBIA, 145, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(FORWARD_LEFT_FEMUR, 165, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_FEMUR, 90, 15, 5);
    smooth_servo(FORWARD_RIGHT_TIBIA, 35, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(FORWARD_RIGHT_FEMUR, 15, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_COXA, 145, 105, 5);
    smooth_servo(FORWARD_LEFT_COXA, 20, 60, 5);
    smooth_servo(BACKWARD_LEFT_COXA, 35, 105, 5);
    smooth_servo(BACKWARD_RIGHT_COXA, 130, 60, 5);
}

// =====================================================
// TEST
// =====================================================

void robot_test_cycle()
{
    smooth_servo(FORWARD_RIGHT_COXA, 105, 75, 5);
    smooth_servo(BACKWARD_RIGHT_COXA, 60, 30, 5);
    smooth_servo(BACKWARD_LEFT_COXA, 105, 135, 5);
    smooth_servo(FORWARD_LEFT_COXA, 60, 90, 5);

    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_LEFT_FEMUR, 90, 165, 5);
    smooth_servo(FORWARD_LEFT_COXA, 90, 60, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(FORWARD_LEFT_FEMUR, 165, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(BACKWARD_LEFT_FEMUR, 90, 15, 5);
    smooth_servo(BACKWARD_LEFT_COXA, 135, 105, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(BACKWARD_LEFT_FEMUR, 15, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_FEMUR, 90, 15, 5);
    smooth_servo(FORWARD_RIGHT_COXA, 75, 105, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(FORWARD_RIGHT_FEMUR, 15, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(BACKWARD_RIGHT_FEMUR, 90, 165, 5);
    smooth_servo(BACKWARD_RIGHT_COXA, 30, 60, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
    smooth_servo(BACKWARD_RIGHT_FEMUR, 165, 90, 5);
    vTaskDelay(pdMS_TO_TICKS(100));
}

// =====================================================
// DANCE ANIMATION
// =====================================================

void robot_dance_cycle()
{
    set_servo(FORWARD_RIGHT_TIBIA, 90);
    set_servo(BACKWARD_RIGHT_TIBIA, 20);
    set_servo(BACKWARD_LEFT_TIBIA, 90);
    set_servo(FORWARD_LEFT_TIBIA, 20);

    vTaskDelay(pdMS_TO_TICKS(250));

    set_servo(FORWARD_RIGHT_TIBIA, 20);
    set_servo(BACKWARD_RIGHT_TIBIA, 90);
    set_servo(BACKWARD_LEFT_TIBIA, 20);
    set_servo(FORWARD_LEFT_TIBIA, 90);

    vTaskDelay(pdMS_TO_TICKS(250));
}

// =====================================================
// PREPARE TO SLEEP
// =====================================================

void robot_prepare_to_sleep() {
    robot_stay_position();

    vTaskDelay(pdMS_TO_TICKS(200));

    smooth_servo(FORWARD_RIGHT_FEMUR, 90, 5, 5);
    smooth_servo(FORWARD_LEFT_FEMUR, 90, 175, 5);
    smooth_servo(BACKWARD_RIGHT_FEMUR, 90, 175, 5);
    smooth_servo(BACKWARD_LEFT_FEMUR, 90, 5, 5);

    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_TIBIA, 90, 160, 5);
    smooth_servo(FORWARD_LEFT_TIBIA, 90, 20, 5);
    smooth_servo(BACKWARD_RIGHT_TIBIA, 90, 20, 5);
    smooth_servo(BACKWARD_LEFT_TIBIA, 90, 160, 5);

    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_FEMUR, 5, 90, 5);
    smooth_servo(FORWARD_LEFT_FEMUR, 175, 90, 5);
    smooth_servo(BACKWARD_RIGHT_FEMUR, 175, 90, 5);
    smooth_servo(BACKWARD_LEFT_FEMUR, 5, 90, 5);

    current_mode = MODE_SLEEPING;
}

// =====================================================
// WAKE UP
// =====================================================

void robot_wake_up() {
    smooth_servo(FORWARD_RIGHT_FEMUR, 90, 5, 5);
    smooth_servo(FORWARD_RIGHT_TIBIA, 160, 90, 5);

    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(BACKWARD_RIGHT_FEMUR, 90, 175, 5);
    smooth_servo(BACKWARD_RIGHT_TIBIA, 20, 90, 5);

    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_LEFT_FEMUR, 90, 175, 5);
    smooth_servo(FORWARD_LEFT_TIBIA, 20, 90, 5);

    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(BACKWARD_LEFT_FEMUR, 90, 5, 5);
    smooth_servo(BACKWARD_LEFT_TIBIA, 160, 90, 5);

    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_FEMUR, 5, 90, 5);
    smooth_servo(BACKWARD_RIGHT_FEMUR, 175, 90, 5);
    smooth_servo(FORWARD_LEFT_FEMUR, 175, 90, 5);
    smooth_servo(BACKWARD_LEFT_FEMUR, 5, 90, 5);

    current_mode = MODE_INIT;
}

// =====================================================
// GO TO MAMA
// =====================================================

void robot_go_to_mama() {
    robot_prepare_to_sleep();

    smooth_servo(FORWARD_RIGHT_FEMUR, 90, 5, 5);
    smooth_servo(FORWARD_LEFT_FEMUR, 90, 175, 5);
    smooth_servo(BACKWARD_RIGHT_FEMUR, 90, 175, 5);
    smooth_servo(BACKWARD_LEFT_FEMUR, 90, 5, 5);

    vTaskDelay(pdMS_TO_TICKS(100));

    set_servo(FORWARD_RIGHT_COXA, 160);
    set_servo(FORWARD_LEFT_COXA, 5);
    set_servo(BACKWARD_RIGHT_COXA, 5);
    set_servo(BACKWARD_LEFT_COXA, 160);

    vTaskDelay(pdMS_TO_TICKS(100));

    smooth_servo(FORWARD_RIGHT_TIBIA, 160, 20, 5);
    smooth_servo(FORWARD_LEFT_TIBIA, 20, 160, 5);
    smooth_servo(BACKWARD_RIGHT_TIBIA, 20, 160, 5);
    smooth_servo(BACKWARD_LEFT_TIBIA, 160, 20, 5);

    current_mode = MODE_BOX;
}

// =====================================================
// HTTP
// =====================================================

static esp_err_t ping_handler(httpd_req_t *req) {
    httpd_resp_send(req, "PING", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t dance_handler(httpd_req_t *req) {
    if (current_mode == MODE_SLEEPING) {
        httpd_resp_set_status(req, HTTPD_400);
        httpd_resp_send(req, "DANCE FAILED", HTTPD_RESP_USE_STRLEN);
        return ESP_FAIL;
    }
    current_mode = MODE_DANCE;
    httpd_resp_send(req, "DANCE MODE", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t move_handler(httpd_req_t *req) {
    if (current_mode == MODE_SLEEPING) {
        httpd_resp_set_status(req, HTTPD_400);
        httpd_resp_send(req, "MOVE FAILED", HTTPD_RESP_USE_STRLEN);
        return ESP_FAIL;
    }
    current_mode = MODE_MOVE;
    httpd_resp_send(req, "MOVE MODE", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t go_to_mama_handler(httpd_req_t *req) {
    if (current_mode == MODE_SLEEPING) {
        httpd_resp_set_status(req, HTTPD_400);
        httpd_resp_send(req, "GO TO MAMA FAILED", HTTPD_RESP_USE_STRLEN);
        return ESP_FAIL;    
    }
    current_mode = MODE_GO_TO_MAMA;
    httpd_resp_send(req, "MODE GO TO MAMA", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t stay_handler(httpd_req_t *req) {
    current_mode = MODE_INIT;
    httpd_resp_send(req, "STAY", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t test_handler(httpd_req_t *req) {
    if (current_mode == MODE_SLEEPING) {
        httpd_resp_set_status(req, HTTPD_400);
        httpd_resp_send(req, "ZOMBIE FAILED", HTTPD_RESP_USE_STRLEN);
        return ESP_FAIL;
    }
    current_mode = MODE_TEST;
    httpd_resp_send(req, "TEST DONE", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t sleep_handler(httpd_req_t *req) {
    if (current_mode == MODE_SLEEPING) {
        httpd_resp_set_status(req, HTTPD_400);
        httpd_resp_send(req, "SLEEP AGAIN?!", HTTPD_RESP_USE_STRLEN);
        return ESP_FAIL;
    }
    current_mode = MODE_PREPARE_TO_SLEEP;
    httpd_resp_send(req, "PREPARE TO SLEEP", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

static esp_err_t wake_up_handler(httpd_req_t *req) {
    if (current_mode != MODE_SLEEPING) {
        httpd_resp_set_status(req, HTTPD_400);
        httpd_resp_send(req, "WAKE UP FAILED", HTTPD_RESP_USE_STRLEN);
        return ESP_FAIL;    
    }
    current_mode = MODE_WAKE_UP;
    httpd_resp_send(req, "WAKE UP", HTTPD_RESP_USE_STRLEN);
    return ESP_OK;
}

httpd_handle_t start_webserver(void)
{
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();
    httpd_handle_t server = NULL;
    if (httpd_start(&server, &config) == ESP_OK)
    {
        httpd_uri_t ping_uri = {
            .uri = "/",
            .method = HTTP_GET,
            .handler = ping_handler,
            .user_ctx = NULL
        };

        httpd_uri_t dance_uri = {
            .uri = "/dance",
            .method = HTTP_GET,
            .handler = dance_handler,
            .user_ctx = NULL
        };

        httpd_uri_t move_uri = {
            .uri = "/move",
            .method = HTTP_GET,
            .handler = move_handler,
            .user_ctx = NULL
        };

        httpd_uri_t go_to_mama_uri = {
            .uri = "/go-to-mama",
            .method = HTTP_GET,
            .handler = go_to_mama_handler,
            .user_ctx = NULL
        };

        httpd_uri_t stay_uri = {
            .uri = "/stay",
            .method = HTTP_GET,
            .handler = stay_handler,
            .user_ctx = NULL
        };

        httpd_uri_t test_uri = {
            .uri = "/test",
            .method = HTTP_GET,
            .handler = test_handler,
            .user_ctx = NULL
        };
        
        httpd_uri_t sleep_uri = {
            .uri = "/sleep",
            .method = HTTP_GET,
            .handler = sleep_handler,
            .user_ctx = NULL
        };

        httpd_uri_t wake_up_uri = {
            .uri = "/wake-up",
            .method = HTTP_GET,
            .handler = wake_up_handler,
            .user_ctx = NULL
        };

        httpd_register_uri_handler(server, &ping_uri);
        httpd_register_uri_handler(server, &dance_uri);
        httpd_register_uri_handler(server, &move_uri);
        httpd_register_uri_handler(server, &go_to_mama_uri);
        httpd_register_uri_handler(server, &stay_uri);
        httpd_register_uri_handler(server, &test_uri);
        httpd_register_uri_handler(server, &sleep_uri);
        httpd_register_uri_handler(server, &wake_up_uri);

        ESP_LOGI(TAG, "HTTP server started");
    }

    return server;
}

// =====================================================
// WIFI AP
// =====================================================

void wifi_init_softap(void)
{
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_ap();
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));
    wifi_config_t wifi_config = {
        .ap = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
            .ssid_len = strlen(WIFI_SSID),
            .channel = 1,
            .max_connection = MAX_STA_CONN,
            .authmode = WIFI_AUTH_WPA_WPA2_PSK,
        },
    };
    ESP_ERROR_CHECK(
        esp_wifi_set_mode(WIFI_MODE_AP)
    );
    ESP_ERROR_CHECK(
        esp_wifi_set_config(WIFI_IF_AP, &wifi_config)
    );
    ESP_ERROR_CHECK(esp_wifi_start());
    ESP_LOGI(TAG,
             "WiFi AP started: %s",
             WIFI_SSID);
}

// =====================================================
// MAIN
// =====================================================

void app_main(void)
{
    esp_err_t ret = nvs_flash_init();

    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND)
    {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }

    ESP_ERROR_CHECK(ret);
    ESP_ERROR_CHECK(i2c_master_init());

    pca9685_init();
    robot_stay_position();
    wifi_init_softap();
    start_webserver();

    while (1)
    {
        switch (current_mode)
        {
            case MODE_MOVE:
                robot_move_cycle();
                break;
            case MODE_GO_TO_MAMA:
                robot_go_to_mama();
                break;
            case MODE_DANCE:
                robot_dance_cycle();
                break;
            case MODE_INIT:
                robot_stay_position();
                break;
            case MODE_TEST:
                robot_test_cycle();
                break;
            case MODE_PREPARE_TO_SLEEP:
                robot_prepare_to_sleep();
                break;
            case MODE_WAKE_UP:
                robot_wake_up();
                break;
            case MODE_SLEEPING:
            case MODE_BOX:
            default:
                vTaskDelay(pdMS_TO_TICKS(100));
                break;
        }
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}
