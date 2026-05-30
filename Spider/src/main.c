#include <stdio.h>
#include <math.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "esp_log.h"

#define I2C_MASTER_SCL_IO           5
#define I2C_MASTER_SDA_IO           4
#define I2C_MASTER_NUM              I2C_NUM_0
#define I2C_MASTER_FREQ_HZ          100000

#define PCA9685_ADDR                0x40

#define MODE1                       0x00
#define PRESCALE                    0xFE
#define LED0_ON_L                   0x06

#define SERVO_MIN                   102
#define SERVO_MAX                   410

static const char *TAG = "PCA9685";


// ====================== I2C ======================

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

    return i2c_driver_install(
        I2C_MASTER_NUM,
        conf.mode,
        0,
        0,
        0
    );
}


// ====================== PCA9685 ======================

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
    // sleep
    pca9685_write(MODE1, 0x10);

    // Частота 50 Гц
    float freq = 50.0;
    uint8_t prescale_val = (uint8_t)(round(25000000.0 / (4096.0 * freq)) - 1);

    pca9685_write(PRESCALE, prescale_val);

    // Wake up
    pca9685_write(MODE1, 0x20);

    vTaskDelay(pdMS_TO_TICKS(10));

    for (int i = 0; i < 16; i++) {
        pca9685_set_pwm(i, 0, 0);
    }

    vTaskDelay(pdMS_TO_TICKS(100));

    ESP_LOGI(TAG, "PCA9685 initialized");
}


// ====================== Servo ======================

uint16_t angle_to_pwm(int angle)
{
    if (angle < 0) angle = 0;
    if (angle > 180) angle = 180;

    return SERVO_MIN +
           ((SERVO_MAX - SERVO_MIN) * angle) / 180;
}

void set_servo(uint8_t channel, int angle) {
    uint16_t pwm = angle_to_pwm(angle);
    pca9685_set_pwm(channel, 0, pwm);
    ESP_LOGI(TAG, "CH %d -> angle %d -> pwm %d", channel, angle, pwm);
}

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

void smooth_servo(uint8_t ch, int from, int to, int step_delay) {
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

// ====================== Main ======================

void app_main(void)
{
    ESP_ERROR_CHECK(i2c_master_init());
    vTaskDelay(pdMS_TO_TICKS(100));

    pca9685_init();

    vTaskDelay(pdMS_TO_TICKS(100));

    // Начальные позиции

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

    vTaskDelay(pdMS_TO_TICKS(1500));

    while (1)
    {
        // =====================================================
        // ФАЗА 1
        // Передние ноги вытягиваем вперед
        // =====================================================

        // поднять переднюю правую
        smooth_servo(FORWARD_RIGHT_TIBIA, 90, 35, 10);

        // вынести вперед
        smooth_servo(FORWARD_RIGHT_COXA, 105, 145, 10);

        // опустить
        smooth_servo(FORWARD_RIGHT_TIBIA, 145, 90, 10);

        vTaskDelay(pdMS_TO_TICKS(100));


        // поднять переднюю левую
        smooth_servo(FORWARD_LEFT_TIBIA, 90, 145, 10);

        // вынести вперед
        smooth_servo(FORWARD_LEFT_COXA, 60, 20, 10);

        // опустить
        smooth_servo(FORWARD_LEFT_TIBIA, 145, 90, 10);

        vTaskDelay(pdMS_TO_TICKS(200));


        // =====================================================
        // ФАЗА 2
        // Задние ноги толкают корпус вперед
        // =====================================================

        smooth_servo(BACKWARD_RIGHT_COXA, 60, 130, 12);
        smooth_servo(BACKWARD_LEFT_COXA, 105, 40, 12);

        vTaskDelay(pdMS_TO_TICKS(250));


        // =====================================================
        // ФАЗА 3
        // Подтягиваем задние ноги
        // =====================================================

        // задняя правая
        smooth_servo(BACKWARD_RIGHT_TIBIA, 90, 145, 10);

        smooth_servo(BACKWARD_RIGHT_COXA, 130, 60, 10);

        smooth_servo(BACKWARD_RIGHT_TIBIA, 145, 90, 10);

        vTaskDelay(pdMS_TO_TICKS(100));


        // задняя левая
        smooth_servo(BACKWARD_LEFT_TIBIA, 90, 145, 10);

        smooth_servo(BACKWARD_LEFT_COXA, 40, 105, 10);

        smooth_servo(BACKWARD_LEFT_TIBIA, 145, 90, 10);

        vTaskDelay(pdMS_TO_TICKS(200));


        // =====================================================
        // ФАЗА 4
        // Возвращаем передние ноги чуть назад
        // чтобы был новый цикл
        // =====================================================

        smooth_servo(FORWARD_RIGHT_COXA, 145, 105, 12);
        smooth_servo(FORWARD_LEFT_COXA, 20, 60, 12);

        vTaskDelay(pdMS_TO_TICKS(250));
    }
}
