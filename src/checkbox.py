import pygame

from src.button import Button


class CheckBox(Button):
    def __init__(
        self, pos: tuple[int, int], size: tuple[int, int], default_value: bool
    ):
        super().__init__(pos, size)
        self._value = default_value
        return

    @property
    def value(self) -> bool:
        return self._value

    @value.setter
    def value(self, new: bool):
        self._value = new
        return

    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    def render(self, surface: pygame.Surface):
        if self._is_pushed:
            color = (200, 200, 200)
        else:
            color = (255, 255, 255)

        pygame.draw.rect(surface, color, self._rect)
        pygame.draw.rect(surface, (0, 0, 0), self._rect, 0 if self._value else 2)
        return
