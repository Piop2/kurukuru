import pygame
import win32gui
import win32con
import win32api


class Animation:
    def __init__(self, images: list[pygame.Surface], duration: int):
        self.images = images
        self.durations = duration

        self.frame = 0
        self.timer = 0
        return

    def get_image(self) -> pygame.Surface:
        return self.images[self.frame]

    def update(self, dt: int):
        self.timer += dt
        if self.timer >= self.durations:
            self.frame += 1
            if self.frame == len(self.images) - 1:
                self.frame = 0
            self.timer = 0
        return


def get_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


class SurroundAudio:
    def __init__(self, sound: pygame.mixer.Sound, chan: int, window_size: tuple[int, int]):
        self.sound = sound
        self.channel = pygame.mixer.Channel(chan)
        self.window_size = window_size

        self.left_ear = (window_size[0] / 9 * 3, window_size[1] - 500)
        self.right_ear = (window_size[0] / 9 * 6, window_size[1] - 500)

        self.channel.play(self.sound, -1)
        return

    def update(self, pos: list[float, float], master_volume: int = 1):
        left = (self.window_size[0] - get_distance(pos, self.left_ear)) / self.window_size[0] / 2 * master_volume
        right = (self.window_size[0] - get_distance(pos, self.right_ear)) / self.window_size[0] / 2 * master_volume
        self.channel.set_volume(left, right)
        return


class Main:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load("resource/icon.png"))
        pygame.display.set_caption("kurukuru v1.1")

        self.background = (255, 0, 128)
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                               win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*self.background), 0, win32con.LWA_COLORKEY)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

        self.pos = [self.screen.get_width(), self.screen.get_height() - 500]
        self.speed = 1
        images = [pygame.image.load(f"resource/{i}.png") for i in range(1, 7)]
        self.animation = Animation(images=images, duration=80)
        sound = pygame.mixer.Sound("resource/kurukuru.wav")
        self.sound = SurroundAudio(sound, 1, self.screen.get_size())

        self.is_mute = False
        return

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)

            self.animation.update(dt)
            self.pos[0] -= self.speed * dt
            if self.pos[0] <= - 500:
                self.pos[0] = self.screen.get_width()
            self.sound.update(self.pos, 1 if not self.is_mute else 0)

            self.screen.fill(self.background)
            self.screen.blit(self.animation.get_image(), self.pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_m:
                        self.is_mute = not self.is_mute
            pygame.display.update()

        pygame.quit()
        return


if __name__ == '__main__':
    Main().run()
