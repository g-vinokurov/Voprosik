import pygame
import requests
import sys
import os
import threading
import glob

pygame.init()

# размеры окна
WINDOW_W = 1280
WINDOW_H = 720
WINDOW_SIZE = (WINDOW_W, WINDOW_H)

# частота кадров
FPS = 60

# префикс для API
BASE_URL = "http://192.168.4.1"

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# курсоры
CURSOR_ARROW = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW)
CURSOR_HAND  = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)

CHECK_CONNECTION_INTERVAL = 3000
connection_status = "Checking..."
connection_color = WHITE

pygame.time.set_timer(pygame.USEREVENT + 1, CHECK_CONNECTION_INTERVAL)


class FontManager:
    def __init__(self):
        self.fonts = {}
    
    def load_font(self, name, path, size):
        try:
            self.fonts[name] = pygame.font.Font(path, size)
            print(f"Шрифт '{name}' загружен")
            return True
        except:
            print(f"Ошибка загрузки '{name}', использую стандартный")
            self.fonts[name] = pygame.font.Font(None, size)
            return False
    
    def get_font(self, name):
        return self.fonts.get(name, pygame.font.Font(None, 24))
    
    def render(self, name, text, color, antialias=True):
        font = self.get_font(name)
        return font.render(text, antialias, color)


fm = FontManager()


class Animation:
    def __init__(self, frames_folder, center_x, center_y, frame_rate = 1):
        self.frames = []

        for filepath in sorted(glob.glob(f"animations/{frames_folder}/img-??.png")):
            frame = pygame.image.load(filepath)
            frame = pygame.transform.smoothscale(frame, (WINDOW_W / 2, WINDOW_H / 2))
            frame_rect = frame.get_rect(center=(center_x, center_y))
            self.frames.append((frame, frame_rect))
        
        if not self.frames:
            raise ValueError("No frames")
        
        self.time_counter = 0
        self.frame_counter = 0
        self.frame_rate = round(FPS * frame_rate)
        
    def play(self, surface: pygame.Surface):
        if self.time_counter > self.frame_rate:
            self.time_counter = 0
            self.frame_counter = (self.frame_counter + 1) % len(self.frames)
        else:
            self.time_counter += 1
        frame, frame_rect = self.frames[self.frame_counter]
        surface.blit(frame, frame_rect)


animation = None


class ActionButton:
    def __init__(self, center_x, center_y, width, height, text, font, font_color, on_hover = None, on_click = None, disabled = False):
        self.width  = width
        self.height = height
        self.on_hover = on_hover
        self.on_click = on_click

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.surface, (0, 0, 0, 150), self.surface.get_rect(), border_radius=16)
        self.rect = self.surface.get_rect(center=(center_x, center_y))

        self.hovered_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.hovered_surface, (0, 0, 0, 100), self.hovered_surface.get_rect(), border_radius=16)
        self.hovered_surface_rect = self.hovered_surface.get_rect(center=(center_x, center_y))

        self.text_surface = fm.render(font, text, font_color)
        self.text_surface_rect = self.text_surface.get_rect(center=(center_x, center_y))

        self.is_hovered = False
        self.is_disabled = disabled

    def draw(self, surface):
        if self.is_hovered and not self.is_disabled:
            surface.blit(self.hovered_surface, self.hovered_surface_rect)
        else:
            surface.blit(self.surface, self.rect)
        surface.blit(self.text_surface, self.text_surface_rect)

    def update_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

# отправка команды роботу
def send_get_request(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    try:
        print(f"Отправка запроса: {url}")
        response = requests.get(url, timeout=5)
        print(f"Ответ ({response.status_code}): {response.text}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {e}")
        return False

# обработка действия для робота
def do_action(endpoint, action_animation: Animation):
    global animation

    def send():
        try:
            send_get_request(endpoint)
        except:
            pass
        
    thread = threading.Thread(target=send)
    thread.daemon = True
    thread.start()

    animation = action_animation

# проверка соединения с роботом
def check_connection():
    def _check():
        global connection_status, connection_color
        try:
            response = requests.get(f"{BASE_URL}/", timeout=2)
            if response.status_code == 200:
                connection_status = "Voprosik is on-line"
                connection_color = (0, 255, 0)
            else:
                connection_status = f"Error: {response.status_code}"
                connection_color = (255, 255, 0)
        except:
            connection_status = "Not connected!"
            connection_color = (255, 0, 0)
    
    threading.Thread(target=_check, daemon=True).start()

# основная программа
def main():
    # Создание окна
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Voprosik Control")

    clock = pygame.time.Clock()

    # загружаем фон
    if os.path.exists("spiders.png"):
        background = pygame.image.load("spiders.png")
        background = pygame.transform.scale(background, WINDOW_SIZE)
    else:
        print("Файл фона spiders.png не найден!")
        background = pygame.Surface(WINDOW_SIZE)
        background.fill(WHITE)

    # загружаем шрифты
    fm.load_font("actions", "MetalMania-Regular.ttf", 40)
    fm.load_font("action", "MetalMania-Regular.ttf", 36)
    fm.load_font("message", "MetalMania-Regular.ttf", 30)

    actions_label = ActionButton(
        center_x   = WINDOW_W / 4,
        center_y   = WINDOW_H / 4,
        width      = WINDOW_W / 3,
        height     = 80,
        text       = "Actions",
        font       = "actions",
        font_color = WHITE,
        disabled   = True
    )

    # кнопки
    buttons = [
        ActionButton(
            center_x   = WINDOW_W / 4 - WINDOW_W / 12,
            center_y   = WINDOW_H / 4 + 40 + 30 + 20,
            width      = WINDOW_W / 6 - 5,
            height     = 60,
            text       = "Stay!",
            font       = "action",
            font_color = WHITE,
            on_click   = lambda: do_action("stay", Animation("stay", WINDOW_W / 4 * 3, WINDOW_H / 2))
        ),
        ActionButton(
            center_x   = WINDOW_W / 4 + WINDOW_W / 12,
            center_y   = WINDOW_H / 4 + 40 + 30 + 20,
            width      = WINDOW_W / 6 - 5,
            height     = 60,
            text       = "Wake Up!",
            font       = "action",
            font_color = WHITE,
            on_click   = lambda: do_action("wake-up", Animation("wake-up", WINDOW_W / 4 * 3, WINDOW_H / 2, frame_rate=0.75))
        ),
        ActionButton(
            center_x   = WINDOW_W / 4 - WINDOW_W / 12,
            center_y   = WINDOW_H / 4 + 40 + 60 + 30 + 30,
            width      = WINDOW_W / 6 - 5,
            height     = 60,
            text       = "Tsok-Tsok!",
            font       = "action",
            font_color = WHITE,
            on_click   = lambda: do_action("move", Animation("tsok-tsok", WINDOW_W / 4 * 3, WINDOW_H / 2, frame_rate=0.75))
        ),
        ActionButton(
            center_x   = WINDOW_W / 4 + WINDOW_W / 12,
            center_y   = WINDOW_H / 4 + 40 + 60 + 30 + 30,
            width      = WINDOW_W / 6 - 5,
            height     = 60,
            text       = "Zombie!",
            font       = "action",
            font_color = WHITE,
            on_click   = lambda: do_action("test", Animation("zombie", WINDOW_W / 4 * 3, WINDOW_H / 2, frame_rate=0.75))
        ),
        ActionButton(
            center_x   = WINDOW_W / 4,
            center_y   = WINDOW_H / 4 + 40 + 60 + 60 + 30 + 40,
            width      = WINDOW_W / 6 - 5,
            height     = 60,
            text       = "Dance!",
            font       = "action",
            font_color = WHITE,
            on_click   = lambda: do_action("dance", Animation("dance", WINDOW_W / 4 * 3, WINDOW_H / 2, frame_rate=0.5))
        ),
        ActionButton(
            center_x   = WINDOW_W / 4,
            center_y   = WINDOW_H / 4 + 40 + 60 + 60 + 60 + 30 + 50,
            width      = WINDOW_W / 6 - 5,
            height     = 60,
            text       = "Sleep...",
            font       = "action",
            font_color = WHITE,
            on_click   = lambda: do_action("sleep", Animation("sleep", WINDOW_W / 4 * 3, WINDOW_H / 2))
        ),
    ]

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        if any([button.update_hover(mouse_pos) for button in buttons]):
            pygame.mouse.set_cursor(CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(CURSOR_ARROW)
        
        for event in pygame.event.get():
            # обработка закрытия окна
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # нажали левой кнопкой мыши
                if event.button == 1:
                    for button in buttons:
                        # попали по кнопке
                        if button.is_hovered:
                            button.on_click()
            elif event.type == pygame.USEREVENT + 1:
                check_connection()

        # отрисовка фона
        screen.blit(background, (0, 0))
        
        # Заголовок
        actions_label.draw(screen)

        # отрисовка кнопок
        for button in buttons:
            button.draw(screen)
        
        if animation is not None:
            animation.play(screen)
        
        message = fm.render("message", connection_status, connection_color)
        message_rect = message.get_rect(center=(WINDOW_W / 2, WINDOW_H / 4 * 3))
        screen.blit(message, message_rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
