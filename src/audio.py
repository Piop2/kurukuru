import pygame


def _get_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


class SurroundAudio:
    def __init__(self, sound: pygame.mixer.Sound, chan: int, window_size: tuple[int, int]):
        self.sound = sound
        self.channel = pygame.mixer.Channel(chan)
        self.window_size = window_size

        self.left_ear = (window_size[0] / 9 * 3, window_size[1] - 500)
        self.right_ear = (window_size[0] / 9 * 6, window_size[1] - 500)
        return

    def play(self):
        self.channel.play(self.sound, -1)
        return

    def stop(self):
        self.channel.stop()
        return

    def update(self, pos: list[float, float], master_volume: int = 1):
        left = (self.window_size[0] - _get_distance(pos, self.left_ear)) / self.window_size[0] / 2 * master_volume
        right = (self.window_size[0] - _get_distance(pos, self.right_ear)) / self.window_size[0] / 2 * master_volume
        self.channel.set_volume(left, right)
        return
