import pygame


def _get_distance(pos1, pos2):
    return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


class SurroundAudio:
    def __init__(
        self, sound: pygame.mixer.Sound, chan: int, window_size: tuple[int, int]
    ):
        self.sound = sound
        self.channel = pygame.mixer.Channel(chan)
        self.window_size = window_size

        self.left_ear = (window_size[0] / 9 * 3, window_size[1] - 500)
        self.right_ear = (window_size[0] / 9 * 6, window_size[1] - 500)

        self.volume = 1
        self.surround_audio = True
        return

    def play(self, volume, loop=False):
        self.volume = volume
        self.channel.set_volume(volume)
        self.channel.play(self.sound, -1 if loop else 0)
        return

    def stop(self):
        self.channel.stop()
        return

    def update(self, pos: list[float, float]):
        if self.surround_audio:
            left = (
                (self.window_size[0] - _get_distance(pos, self.left_ear))
                / self.window_size[0]
                / 2
                * self.volume
            )
            if left <= 0:
                left = 0
            right = (
                (self.window_size[0] - _get_distance(pos, self.right_ear))
                / self.window_size[0]
                / 2
                * self.volume
            )
            if right <= 0:
                right = 0
        else:
            left = self.volume
            right = self.volume
        self.channel.set_volume(left, right)
        return
