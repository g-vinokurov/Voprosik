import pygame
import requests
import sys

# Инициализация Pygame
pygame.init()

# Константы
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_MARGIN = 20
BASE_URL = "http://192.168.4.1"

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 100, 255)
GREEN = (0, 200, 0)
RED = (255, 50, 50)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
DARK_RED = (0xd3, 0, 0)


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=10)  # Border
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

def send_get_request(endpoint):
    """Отправляет GET-запрос на указанный endpoint"""
    url = f"{BASE_URL}/{endpoint}"
    try:
        print(f"Отправка запроса: {url}")
        response = requests.get(url, timeout=5)
        print(f"Ответ ({response.status_code}): {response.text}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return False

def main():
    # Создание окна
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("ESP32 Control Interface")
    clock = pygame.time.Clock()

    # Создание кнопок
    buttons = {
        'Init': Button(
            WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
            50,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Init",
            BLUE,
            LIGHT_BLUE
        ),
        'Ping': Button(
            WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
            120,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Ping",
            GREEN,
            LIGHT_GREEN
        ),
        'Move': Button(
            WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
            190,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Move",
            RED,
            LIGHT_RED
        ),
        'Fast-Move': Button(
            WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
            260,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Fast Move",
            DARK_RED,
            RED
        ),
        'Test': Button(
            WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2,
            330,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
            "Test",
            BLACK,
            GRAY
        )
    }

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    for button_name, button in buttons.items():
                        if button.is_clicked(mouse_pos):
                            print(f"\nНажата кнопка: {button_name}")
                            send_get_request(button_name.lower())

        # Обновление состояния кнопок при наведении
        for button in buttons.values():
            button.check_hover(mouse_pos)

        # Отрисовка
        screen.fill(WHITE)
        
        # Заголовок
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("ESP32 Control", True, BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 25))
        screen.blit(title_text, title_rect)

        # Отрисовка кнопок
        for button in buttons.values():
            button.draw(screen)

        # Инструкция внизу
        info_font = pygame.font.Font(None, 20)
        info_text = info_font.render("Click buttons to send commands to ESP32", True, GRAY)
        info_rect = info_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 20))
        screen.blit(info_text, info_rect)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()