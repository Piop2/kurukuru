import pygame


class Animation:
    def __init__(self, images: list[pygame.Surface], duration: int, speed: float = 1.0):
        self._images = images
        self._durations = duration

        self._frame = 0
        self._timer = 0

        self.speed = speed
        return

    def get_image(self) -> pygame.Surface:
        return self._images[self._frame]

    def update(self, dt: int):
        self._timer += dt * self.speed
        if self._timer >= self._durations:
            self._frame += 1
            if self._frame == len(self._images) - 1:
                self._frame = 0
            self._timer = 0
        return
