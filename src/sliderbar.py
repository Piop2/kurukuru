import pygame


class SliderBar:
    def __init__(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        max_value: int,
        min_value: int,
        default_value: int,
    ):
        self._pos = pos
        self._size = size
        self._rect = pygame.Rect(*pos, *size)

        self._min_value = min_value
        self._max_value = max_value
        self._value = default_value

        self._is_grabbed = False
        self._is_hovered = False

        self._button_w = size[1]

        self._unit = (self._size[0] - self._button_w) / (
            self._max_value - self._min_value
        )
        return

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, new: int):
        self._value = new
        return

    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    def update(self, mouse_pos: tuple[int, int], is_click: bool) -> None:
        if not is_click:
            if self._rect.collidepoint(mouse_pos):
                self._is_hovered = True
            else:
                self._is_hovered = False
            self._is_grabbed = False
            return

        if self._is_grabbed:
            d = mouse_pos[0] - self._pos[0] - (self._button_w / 2)
            if d <= 0:
                new_value = self._min_value
            elif d >= self._size[0] - self._button_w:
                new_value = self._max_value
            else:
                new_value = int(d / self._unit)

            self._value = new_value
            return

        if self._is_hovered:
            self._is_grabbed = True
        return

    def render(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (255, 255, 255), self._rect)
        pygame.draw.rect(surface, (0, 0, 0), self._rect, 2)

        if self._value == self._min_value:
            button_x = 0
        elif self._value == self._max_value:
            button_x = self._size[0] - self._button_w
        else:
            button_x = self._value * self._unit
        pygame.draw.rect(
            surface,
            (0, 0, 0),
            (self._pos[0] + button_x, self._pos[1], self._button_w, self._button_w),
        )
        return
