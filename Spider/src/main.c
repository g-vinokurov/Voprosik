#include <stdio.h>
#include "driver/i2c.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

// ===== НАСТРОЙКИ I2C =====
#define I2C_MASTER_SCL_IO           5
#define I2C_MASTER_SDA_IO           4
#define I2C_MASTER_NUM              I2C_NUM_0
#define I2C_MASTER_FREQ_HZ          100000
#define PCA9685_ADDR                0x40

// ===== НАСТРОЙКИ ТЕСТОВОГО СВЕТОДИОДА =====
//#define TEST_LED_GPIO               48   // Встроенный LED на многих платах ESP32-S3
#define TEST_LED_GPIO  2   // вместо 48
                                          // Если нет встроенного — любой свободный пин

// ===== РЕГИСТРЫ PCA9685 =====
#define PCA9685_MODE1               0x00
#define PCA9685_MODE2               0x01
#define PCA9685_PRESCALE            0xFE
#define PCA9685_LED0_ON_L           0x06

static const char *TAG = "TEST";

// ===== ФУНКЦИИ PCA9685 =====
esp_err_t pca9685_write_byte(uint8_t reg, uint8_t data) {
    uint8_t buf[2] = {reg, data};
    return i2c_master_write_to_device(I2C_MASTER_NUM, PCA9685_ADDR, 
                                      buf, 2, pdMS_TO_TICKS(100));
}

esp_err_t pca9685_set_pwm(uint8_t channel, uint16_t on, uint16_t off) {
    uint8_t buf[5] = {
        PCA9685_LED0_ON_L + 4 * channel,
        on & 0xFF,
        (on >> 8) & 0xFF,
        off & 0xFF,
        (off >> 8) & 0xFF
    };
    return i2c_master_write_to_device(I2C_MASTER_NUM, PCA9685_ADDR,
                                      buf, 5, pdMS_TO_TICKS(100));
}

void app_main(void)
{
    // ===== 1. НАСТРОЙКА ТЕСТОВОГО СВЕТОДИОДА =====
    gpio_set_direction(TEST_LED_GPIO, GPIO_MODE_OUTPUT);
    
    // Мигаем 3 раза — подтверждение запуска
    for (int i = 0; i < 3; i++) {
        gpio_set_level(TEST_LED_GPIO, 1);
        vTaskDelay(pdMS_TO_TICKS(200));
        gpio_set_level(TEST_LED_GPIO, 0);
        vTaskDelay(pdMS_TO_TICKS(200));
    }
    
    ESP_LOGI(TAG, "=== ТЕСТ СЕРВОПРИВОДОВ С ИНДИКАЦИЕЙ ===");
    ESP_LOGI(TAG, "Светодиод мигает на GPIO %d", TEST_LED_GPIO);
    vTaskDelay(pdMS_TO_TICKS(3000));
    
    // ===== 2. ИНИЦИАЛИЗАЦИЯ I2C =====
    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = I2C_MASTER_SDA_IO,
        .scl_io_num = I2C_MASTER_SCL_IO,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = I2C_MASTER_FREQ_HZ,
    };
    ESP_ERROR_CHECK(i2c_param_config(I2C_MASTER_NUM, &conf));
    ESP_ERROR_CHECK(i2c_driver_install(I2C_MASTER_NUM, I2C_MODE_MASTER, 0, 0, 0));
    
    // ===== 3. ИНИЦИАЛИЗАЦИЯ PCA9685 =====
    ESP_LOGI(TAG, "Инициализация PCA9685...");
    pca9685_write_byte(PCA9685_MODE1, 0x00);
    vTaskDelay(pdMS_TO_TICKS(10));
    pca9685_write_byte(PCA9685_MODE2, 0x04);
    pca9685_write_byte(PCA9685_MODE1, 0x10);  // Sleep
    pca9685_write_byte(PCA9685_PRESCALE, 100); // 60 Гц
    pca9685_write_byte(PCA9685_MODE1, 0x01);  // Normal
    vTaskDelay(pdMS_TO_TICKS(5));
    ESP_LOGI(TAG, "PCA9685 готов!");
    
    // ===== 4. ДИАГНОСТИКА =====
    ESP_LOGI(TAG, "");
    ESP_LOGI(TAG, "╔════════════════════════════════════╗");
    ESP_LOGI(TAG, "║   ДИАГНОСТИКА ЗАПУЩЕНА            ║");
    ESP_LOGI(TAG, "╠════════════════════════════════════╣");
    ESP_LOGI(TAG, "║ LED на GPIO%d мигает при     ║", TEST_LED_GPIO);
    ESP_LOGI(TAG, "║ каждой смене фазы теста          ║");
    ESP_LOGI(TAG, "║                                  ║");
    ESP_LOGI(TAG, "║ Для проверки ШИМ без мультиметра:║");
    ESP_LOGI(TAG, "║ Подключите светодиод (с резисто- ║");
    ESP_LOGI(TAG, "║ ром 220 Ом) между PWM0 и GND     ║");
    ESP_LOGI(TAG, "║ на плате PCA9685.                ║");
    ESP_LOGI(TAG, "╚════════════════════════════════════╝");
    ESP_LOGI(TAG, "");
    
    // ===== 5. ЦИКЛ ТЕСТА =====
    int phase = 0;
    
    while (1) {
        // Мигаем светодиодом при каждой смене фазы
        gpio_set_level(TEST_LED_GPIO, 1);
        vTaskDelay(pdMS_TO_TICKS(100));
        gpio_set_level(TEST_LED_GPIO, 0);
        
        switch (phase) {
            case 0:
                ESP_LOGI(TAG, "━━━ ФАЗА 0: ВСЕ КАНАЛЫ ВЫКЛЮЧЕНЫ (0) ━━━");
                ESP_LOGI(TAG, "Светодиод на PWM0 НЕ горит");
                for (int ch = 0; ch < 12; ch++) {
                    pca9685_set_pwm(ch, 0, 0);  // Полностью выключено
                }
                break;
                
            case 1:
                ESP_LOGI(TAG, "━━━ ФАЗА 1: МИНИМАЛЬНЫЙ СИГНАЛ (150) ━━━");
                ESP_LOGI(TAG, "Светодиод на PWM0 еле светится");
                for (int ch = 0; ch < 12; ch++) {
                    pca9685_set_pwm(ch, 0, 150);
                }
                break;
                
            case 2:
                ESP_LOGI(TAG, "━━━ ФАЗА 2: СРЕДНИЙ СИГНАЛ (375) ━━━");
                ESP_LOGI(TAG, "Светодиод на PWM0 горит в пол-яркости");
                for (int ch = 0; ch < 12; ch++) {
                    pca9685_set_pwm(ch, 0, 375);
                }
                break;
                
            case 3:
                ESP_LOGI(TAG, "━━━ ФАЗА 3: МАКСИМАЛЬНЫЙ СИГНАЛ (600) ━━━");
                ESP_LOGI(TAG, "Светодиод на PWM0 горит ярко");
                for (int ch = 0; ch < 12; ch++) {
                    pca9685_set_pwm(ch, 0, 600);
                }
                break;
                
            case 4:
                ESP_LOGI(TAG, "━━━ ФАЗА 4: ТЕСТ ОДНОГО КАНАЛА (PWM0) ━━━");
                ESP_LOGI(TAG, "Плавное изменение яркости светодиода...");
                // Плавно увеличиваем яркость
                for (int pwm = 0; pwm <= 600; pwm += 30) {
                    pca9685_set_pwm(0, 0, pwm);
                    vTaskDelay(pdMS_TO_TICKS(50));
                }
                // Плавно уменьшаем
                for (int pwm = 600; pwm >= 0; pwm -= 30) {
                    pca9685_set_pwm(0, 0, pwm);
                    vTaskDelay(pdMS_TO_TICKS(50));
                }
                break;
        }
        
        phase++;
        if (phase > 4) phase = 0;
        
        vTaskDelay(pdMS_TO_TICKS(3000));  // Пауза между фазами
    }
}