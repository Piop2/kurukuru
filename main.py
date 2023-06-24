import json

import pygame
import win32gui
import win32con
import win32api

from src.sliderbar import SliderBar
from src.checkbox import CheckBox
from src.button import Button, FloatingButton
from src.animation import Animation
from src.audio import SurroundAudio
from src.outline import perfect_outline


class App:
    def __init__(self):
        with open("setting.json", "r") as f:
            self.config_data = json.load(f)

        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.VERSION = "v2.0b5"
        self.WINDOW_SIZE = (1000, 500)
        self.MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.INVISIBLE_BACKGROUND = (255, 0, 128)
        self.COGNIZANCE = 100

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(f"KURUKURU {self.VERSION}")
        pygame.display.set_icon(pygame.image.load("resource/icon/icon.png"))
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
        images = []
        n = 0
        while True:
            try:
                image = pygame.image.load(f"resource/animation/{n}.png")
            except FileNotFoundError:
                break
            images.append(image)
            n += 1
        self.origin_image_size = images[0].get_size()

        self.ani = Animation(images, 80, self.config_data["animationSpeed"])
        self.grab = False
        self.attached_pos = self.config_data["attached"]

        sound = pygame.mixer.Sound("resource/sound/kurukuru.wav")
        self.mixer = SurroundAudio(sound, 0, self.MONITOR_SIZE)

        # 폰트 크레딧 넣어야 됩니다.
        self.neo_font_37 = pygame.font.Font("resource/font/NeoDunggeunmoPro-Regular.ttf", 37)
        self.neo_font_20 = pygame.font.Font("resource/font/NeoDunggeunmoPro-Regular.ttf", 20)

        self.volume = self.config_data["volume"] / 100
        self.volume_slider = SliderBar(
            (550, 90), (400, 20), 100, 0, self.config_data["volume"]
        )

        self.surround_audio_active = self.config_data["surroundAudio"]
        self.surround_audio_checkbox = CheckBox(
            (550, 125), (20, 20), self.config_data["surroundAudio"]
        )

        self.ani_speed_slider = SliderBar(
            (550, 180), (400, 20), 200, 0, self.config_data["animationSpeed"]
        )

        self.size = self.config_data["size"] / 100
        self.size_slider = SliderBar(
            (550, 230), (400, 20), 200, 0, self.config_data["size"]
        )

        self.speed = self.config_data["speed"] / 100
        self.speed_slider = SliderBar((550, 280), (400, 20), 400, 0, self.config_data["speed"])

        self.top_button = Button((710, 320), (80, 20))
        self.bottom_button = Button((710, 420), (80, 20))
        self.left_button = Button((690, 340), (20, 80))
        self.right_button = Button((790, 340), (20, 80))

        self.reset_button = Button((550, 450), (100, 30))
        self.apply_button = Button((850, 450), (100, 30))

        # kurukuru
        self.setting_button = FloatingButton((self.MONITOR_SIZE[0] // 2 - 100, self.MONITOR_SIZE[1] // 2 - 100), (200, 200))
        self.exit_button = FloatingButton((self.MONITOR_SIZE[0] // 2 - 100, self.MONITOR_SIZE[1] // 8 - 100), (200, 200))
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

    @property
    def image_size(self) -> tuple[float, float]:
        return self.origin_image_size[0] * self.size, self.origin_image_size[1] * self.size

    def save(self):
        with open("setting.json", "w") as f:
            self.config_data["volume"] = self.volume_slider.value
            self.config_data["animationSpeed"] = int(self.ani.speed * 100)
            self.config_data["size"] = self.size_slider.value
            self.config_data["surroundAudio"] = self.surround_audio_active
            self.config_data["speed"] = self.speed_slider.value
            self.config_data["attached"] = self.attached_pos

            json.dump(self.config_data, f, indent=4)
        return

    def run(self):
        mouse_pos = (0, 0)
        mouse_click = False

        cog_alpha = 0

        running = True
        while running:
            dt = self.clock.tick(self.fps)
            mouse_pos = pygame.mouse.get_pos()

            match self.mode:
                case "setting":
                    # update
                    self.ani.update(dt)

                    latest = self.volume
                    self.volume_slider.update(mouse_pos, mouse_click)
                    self.volume = round(self.volume_slider.value / 100, 2)
                    if self.volume != latest:
                        self.mixer.volume = self.volume
                        self.mixer.play(self.volume)

                    self.ani_speed_slider.update(mouse_pos, mouse_click)
                    self.ani.speed = round(self.ani_speed_slider.value / 100, 2)

                    self.size_slider.update(mouse_pos, mouse_click)
                    self.size = round(self.size_slider.value / 100, 2)

                    self.surround_audio_checkbox.update(mouse_pos, mouse_click)
                    self.surround_audio_active = self.surround_audio_checkbox.value

                    self.speed_slider.update(mouse_pos, mouse_click)
                    self.speed = round(self.speed_slider.value / 100, 2)

                    self.top_button.update(mouse_pos, mouse_click)
                    self.bottom_button.update(mouse_pos, mouse_click)
                    self.left_button.update(mouse_pos, mouse_click)
                    self.right_button.update(mouse_pos, mouse_click)

                    if self.top_button.value:
                        self.attached_pos = "top"
                    if self.bottom_button.value:
                        self.attached_pos = "bottom"
                    if self.left_button.value:
                        self.attached_pos = "left"
                    if self.right_button.value:
                        self.attached_pos = "right"

                    self.reset_button.update(mouse_pos, mouse_click)
                    if self.reset_button.value:
                        self.volume_slider.value = 100
                        self.surround_audio_checkbox.value = True
                        self.ani_speed_slider.value = 100
                        self.size_slider.value = 100
                        self.speed_slider.value = 100

                    self.apply_button.update(mouse_pos, mouse_click)
                    if self.apply_button.value:
                        self.save()
                        self.mode = "kurukuru"
                        self.screen = pygame.display.set_mode(self.MONITOR_SIZE, pygame.FULLSCREEN)
                        self.set_window_top()
                        self.mixer.surround_audio = self.surround_audio_active
                        self.mixer.play(self.volume, True)

                        match self.attached_pos:
                            case "bottom":
                                self.pos = [self.MONITOR_SIZE[0], self.MONITOR_SIZE[1] - self.image_size[1]]
                            case "top":
                                self.pos = [- self.image_size[0], 0]
                            case "left":
                                self.pos = [0, self.MONITOR_SIZE[1] - self.image_size[1]]
                            case "right":
                                self.pos = [self.MONITOR_SIZE[0] - self.image_size[0], - self.image_size[1]]

                    # render
                    self.screen.fill((255, 255, 255))

                    title_text = self.neo_font_37.render(f"빙글빙글 f타 {self.VERSION}", True, (0, 0, 0))
                    self.screen.blit(
                        title_text, (750 - (title_text.get_width() // 2), 20)
                    )

                    ani_image = pygame.transform.scale_by(
                        self.ani.get_image(), self.size
                    )
                    self.screen.blit(
                        ani_image,
                        (self.origin_image_size[0] - ani_image.get_width(), self.origin_image_size[1] - ani_image.get_height()),
                    )

                    self.volume_slider.render(self.screen)
                    self.ani_speed_slider.render(self.screen)
                    self.size_slider.render(self.screen)

                    volume_text = self.neo_font_20.render(
                        f"마스터 볼륨: {self.volume_slider.value}%", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        volume_text,
                        (
                            750 - (volume_text.get_width() // 2),
                            self.volume_slider.pos[1] - 20,
                        ),
                    )

                    ani_speed_text = self.neo_font_20.render(
                        f"애니메이션 속도: {self.ani_speed_slider.value}%", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        ani_speed_text,
                        (
                            750 - (ani_speed_text.get_width() // 2),
                            self.ani_speed_slider.pos[1] - 20,
                        ),
                    )

                    size_text = self.neo_font_20.render(
                        f"크기: {self.size_slider.value}%", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        size_text,
                        (
                            750 - (size_text.get_width() // 2),
                            self.size_slider.pos[1] - 20,
                        ),
                    )

                    self.surround_audio_checkbox.render(self.screen)
                    surround_audio_text = self.neo_font_20.render(
                        "서라운드 오디오", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        surround_audio_text,
                        (
                            self.surround_audio_checkbox.pos[0] + 30,
                            self.surround_audio_checkbox.pos[1],
                        ),
                    )

                    self.speed_slider.render(self.screen)
                    speed_text = self.neo_font_20.render(
                        f"속도: {self.speed_slider.value}%", True, (0, 0, 0)
                    )
                    self.screen.blit(
                        speed_text,
                        (
                            750 - (speed_text.get_width() // 2),
                            self.speed_slider.pos[1] - 20,
                        ),
                    )

                    self.top_button.render(self.screen)
                    self.bottom_button.render(self.screen)
                    self.left_button.render(self.screen)
                    self.right_button.render(self.screen)
                    attached_text = self.neo_font_20.render(self.attached_pos, True, (0, 0, 0))
                    self.screen.blit(attached_text, (750 - (attached_text.get_width() // 2), 380 - (attached_text.get_height() // 2)))

                    self.reset_button.render(self.screen)
                    reset_text = self.neo_font_20.render("리셋", True, (0, 0, 0))
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
                    apply_text = self.neo_font_20.render("실행", True, (0, 0, 0))
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
                    self.mixer.update(self.pos)

                    if self.grab:
                        self.pos = [mouse_pos[0] - (self.image_size[0] // 2), mouse_pos[1] - (self.image_size[0] // 4)]
                        self.setting_button.update(mouse_pos, mouse_click)
                        self.exit_button.update(mouse_pos, mouse_click)

                        if mouse_pos[0] <= 0 + self.COGNIZANCE:
                            self.attached_pos = "left"
                        if mouse_pos[0] >= self.MONITOR_SIZE[0] - 1 - self.COGNIZANCE:
                            self.attached_pos = "right"
                        if mouse_pos[1] <= 0 + self.COGNIZANCE:
                            self.attached_pos = "top"
                        if mouse_pos[1] >= self.MONITOR_SIZE[1] - 1 - self.COGNIZANCE:
                            self.attached_pos = "bottom"
                    else:
                        speed = self.speed * dt
                        goto = [0, 0]
                        match self.attached_pos:
                            case "bottom":
                                goto = [- speed, 0]
                                if self.pos[0] <= - self.image_size[0]:
                                    self.pos[0] = self.MONITOR_SIZE[0] + self.image_size[0]
                            case "top":
                                goto = [speed, 0]
                                if self.pos[0] >= self.MONITOR_SIZE[0]:
                                    self.pos[0] = - self.image_size[0]
                            case "left":
                                goto = [0, - speed]
                                if self.pos[1] <= - self.image_size[1]:
                                    self.pos[1] = self.MONITOR_SIZE[1] + self.image_size[1]
                            case "right":
                                goto = [0, speed]
                                if self.pos[1] >= self.MONITOR_SIZE[1]:
                                    self.pos[1] = - self.image_size[1]

                        self.pos = [self.pos[0] + goto[0], self.pos[1] + goto[1]]

                    if pygame.Rect(*self.pos, *self.image_size).collidepoint(mouse_pos):
                        # print(mouse_pos, mouse_click)
                        if mouse_click:
                            self.grab = True
                        else:
                            if self.grab:
                                match self.attached_pos:
                                    case "bottom":
                                        self.pos = [mouse_pos[0] - (self.image_size[0] // 2), self.MONITOR_SIZE[1] - self.image_size[1]]
                                    case "top":
                                        self.pos = [mouse_pos[0] - (self.image_size[0] // 2), 0]
                                    case "left":
                                        self.pos = [0, mouse_pos[1] - (self.image_size[1] // 2)]
                                    case "right":
                                        self.pos = [self.MONITOR_SIZE[0] - self.image_size[0], mouse_pos[1] - (self.image_size[1] // 2)]
                            self.grab = False

                    if self.setting_button.value:
                        self.mode = "setting"
                        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
                        self.mixer.stop()

                    if self.exit_button.value:
                        running = False

                    # render
                    self.screen.fill(self.INVISIBLE_BACKGROUND)

                    ani_image = pygame.transform.scale_by(
                        self.ani.get_image(), self.size
                    )
                    match self.attached_pos:
                        case "bottom":
                            pass
                        case "top":
                            ani_image = pygame.transform.rotate(ani_image, 180)
                        case "left":
                            ani_image = pygame.transform.rotate(ani_image, 270)
                        case "right":
                            ani_image = pygame.transform.rotate(ani_image, 90)

                    if self.grab:
                        self.setting_button.render(self.screen)
                        self.exit_button.render(self.screen)

                        perfect_outline(self.screen, ani_image, self.pos)
                        # ani_image.set_alpha(100)
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

        self.save()
        return


if __name__ == "__main__":
    App().run()
