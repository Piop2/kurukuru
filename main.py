import json

import pygame
import win32gui
import win32con
import win32api

from src.sliderbar import SliderBar
from src.checkbox import CheckBox
from src.button import Button
from src.animation import Animation


class App:
    def __init__(self):
        with open("setting.json", "r") as f:
            self.config_data = json.load(f)

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.VERSION = "v2.0b1"
        self.WINDOW_SIZE = (1000, 500)
        self.MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.INVISIBLE_BACKGROUND = (255, 0, 128)

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(f"KURUKURU {self.VERSION}")
        pygame.display.set_icon(pygame.image.load("resource/icon.png"))
        self.fps = self.config_data["fps"]

        self.mode = "setting"

        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(
            hwnd,
            win32con.GWL_EXSTYLE,
            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED,
        )
        win32gui.SetLayeredWindowAttributes(
            hwnd, win32api.RGB(*self.INVISIBLE_BACKGROUND), 0, win32con.LWA_COLORKEY
        )

        self.pos = [0, 0]
        images = [pygame.image.load(f"resource/{i}.png") for i in range(1, 7)]
        self.ani = Animation(images, 80, self.config_data["animationSpeed"])

        # 폰트 크레딧 넣어야 됩니다.
        self.neo_font_40 = pygame.font.Font("resource/NeoDunggeunmoPro-Regular.ttf", 40)
        self.neo_font_22 = pygame.font.Font("resource/NeoDunggeunmoPro-Regular.ttf", 22)

        self.volume = 1.0
        self.volume_slider = SliderBar(
            (550, 100), (400, 30), 100, 0, self.config_data["volume"]
        )

        self.surround_audio_active = self.config_data["surroundAudio"]
        self.surround_audio_checkbox = CheckBox(
            (550, 150), (25, 25), self.surround_audio_active
        )

        self.ani_speed_slider = SliderBar(
            (550, 220), (400, 30), 200, 0, int(self.config_data["animationSpeed"] * 100)
        )

        self.size = 1.0
        self.size_slider = SliderBar(
            (550, 290), (400, 30), 200, 0, int(self.config_data["size"] * 100)
        )

        self.speed = self.config_data["speed"]
        self.speed_slider = SliderBar((550, 360), (400, 30), 400, 0, int(self.config_data["speed"] * 100))

        self.reset_button = Button((550, 450), (100, 30))
        self.apply_button = Button((850, 450), (100, 30))
        return

    @staticmethod
    def set_window_top():
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOPMOST,
            0,
            0,
            0,
            0,
            win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
            )
        return

    def run(self):
        mouse_pos = (0, 0)
        mouse_click = False

        running = True
        while running:
            dt = self.clock.tick(self.fps)
            mouse_pos = pygame.mouse.get_pos()

            match self.mode:
                case "setting":
                    # update
                    self.ani.update(dt)

                    self.volume_slider.update(mouse_pos, mouse_click)
                    self.volume = round(self.volume_slider.value / 100, 2)

                    self.ani_speed_slider.update(mouse_pos, mouse_click)
                    self.ani.speed = round(self.ani_speed_slider.value / 100, 2)

                    self.size_slider.update(mouse_pos, mouse_click)
                    self.size = round(self.size_slider.value / 100, 2)

                    self.surround_audio_checkbox.update(mouse_pos, mouse_click)
                    self.surround_audio_active = self.surround_audio_checkbox.value

                    self.speed_slider.update(mouse_pos, mouse_click)
                    self.speed = round(self.speed_slider.value / 100, 2)

                    self.reset_button.update(mouse_pos, mouse_click)
                    if self.reset_button.value:
                        self.volume_slider.value = 100
                        self.surround_audio_checkbox.value = True
                        self.ani_speed_slider.value = 100
                        self.size_slider.value = 100
                        self.speed_slider.value = 100

                    self.apply_button.update(mouse_pos, mouse_click)
                    if self.apply_button.value:
                        self.mode = "kurukuru"
                        self.screen = pygame.display.set_mode(self.MONITOR_SIZE, pygame.FULLSCREEN)
                        self.pos = [self.MONITOR_SIZE[0] + 500 * self.size, self.MONITOR_SIZE[1] - 500 * self.size]
                        self.set_window_top()

                    # render
                    self.screen.fill((255, 255, 255))

                    title_text = self.neo_font_40.render(f"빙글빙글 헤르타 {self.VERSION}", True, (0, 0, 0))
                    self.screen.blit(
                        title_text, (750 - (title_text.get_width() // 2), 20)
                    )

                    ani_image = pygame.transform.scale_by(
                        self.ani.get_image(), self.size
                    )
                    self.screen.blit(
                        ani_image,
                        (500 - ani_image.get_width(), 500 - ani_image.get_height()),
                    )

                    self.volume_slider.render(self.screen)
                    self.ani_speed_slider.render(self.screen)
                    self.size_slider.render(self.screen)

                    volume_text = self.neo_font_22.render(
                        f"마스터 볼륨: {self.volume_slider.value}%", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        volume_text,
                        (
                            750 - (volume_text.get_width() // 2),
                            self.volume_slider.pos[1] - 30,
                        ),
                    )

                    ani_speed_text = self.neo_font_22.render(
                        f"애니메이션 속도: x{self.ani.speed:.2f}", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        ani_speed_text,
                        (
                            750 - (ani_speed_text.get_width() // 2),
                            self.ani_speed_slider.pos[1] - 30,
                        ),
                    )

                    size_text = self.neo_font_22.render(
                        f"크기: x{self.size:.2f}", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        size_text,
                        (
                            750 - (size_text.get_width() // 2),
                            self.size_slider.pos[1] - 30,
                        ),
                    )

                    self.surround_audio_checkbox.render(self.screen)
                    surround_audio_text = self.neo_font_22.render(
                        "서라운드 오디오", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        surround_audio_text,
                        (
                            self.surround_audio_checkbox.pos[0] + 50,
                            self.surround_audio_checkbox.pos[1],
                        ),
                    )

                    self.speed_slider.render(self.screen)
                    speed_text = self.neo_font_22.render(
                        f"속도: x{self.speed:.2f}", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        speed_text,
                        (
                            750 - (speed_text.get_width() // 2),
                            self.speed_slider.pos[1] - 30,
                        ),
                    )

                    self.reset_button.render(self.screen)
                    reset_text = self.neo_font_22.render("리셋", True, (0, 0, 0))
                    self.screen.blit(
                        reset_text,
                        (
                            self.reset_button.pos[0]
                            + (self.reset_button.size[0] // 2)
                            - (reset_text.get_width() // 2),
                            self.reset_button.pos[1]
                            + (self.reset_button.size[1] // 2)
                            - (reset_text.get_height() // 2),
                        ),
                    )

                    self.apply_button.render(self.screen)
                    apply_text = self.neo_font_22.render("실행", True, (0, 0, 0))
                    self.screen.blit(
                        apply_text,
                        (
                            self.apply_button.pos[0]
                            + (self.apply_button.size[0] // 2)
                            - (apply_text.get_width() // 2),
                            self.apply_button.pos[1]
                            + (self.apply_button.size[1] // 2)
                            - (apply_text.get_height() // 2),
                        ),
                    )
                case "kurukuru":
                    # update
                    self.ani.update(dt)

                    self.pos[0] -= self.speed * dt
                    if self.pos[0] <= - 500 * self.size:
                        self.pos[0] = self.MONITOR_SIZE[0] + 500 * self.size

                    # render
                    self.screen.fill(self.INVISIBLE_BACKGROUND)

                    ani_image = pygame.transform.scale_by(
                        self.ani.get_image(), self.size
                    )
                    self.screen.blit(
                        ani_image,
                        self.pos,
                    )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # keyboard
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                # mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_click = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        mouse_click = False
            pygame.display.update()

        pygame.quit()

        with open("setting.json", "w") as f:
            self.config_data["volume"] = self.volume_slider.value
            self.config_data["animationSpeed"] = self.ani.speed
            self.config_data["size"] = self.size
            self.config_data["surroundAudio"] = self.surround_audio_active
            self.config_data["speed"] = self.speed

            json.dump(self.config_data, f, indent=4)
        return


if __name__ == "__main__":
    App().run()
