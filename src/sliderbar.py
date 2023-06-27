import pygame


class SliderBar:
    def __init__(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        max_value: int,
        min_value: int,
        default_value: int,
        button_image: pygame.Surface | None = None,
        bar_image: pygame.Surface | None = None,
    ):
        if button_image is not None:
            button_image = button_image.copy()
        if bar_image is not None:
            bar_image = bar_image.copy()

        self._button_image = button_image
        self._bar_image = bar_image

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
        if self._bar_image is not None:
            surface.blit(
                self._bar_image,
                (
                    self._pos[0]
                    + (self._size[0] // 2)
                    - (self._bar_image.get_width() // 2),
                    self._pos[1]
                    + (self._size[1] // 2)
                    - (self._bar_image.get_height() // 2),
                ),
            )
        else:
            pygame.draw.rect(surface, (255, 255, 255), self._rect)
            pygame.draw.rect(surface, (0, 0, 0), self._rect, 2)

        if self._value == self._min_value:
            button_x = 0
        elif self._value == self._max_value:
            button_x = self._size[0] - self._button_w
        else:
            button_x = self._value * self._unit

        pos = (self._pos[0] + button_x, self._pos[1])
        size = (self._button_w, self._button_w)

        if self._button_image is not None:
            surface.blit(
                self._button_image,
                (
                    pos[0] + (size[0] // 2) - (self._button_image.get_width() // 2),
                    pos[1] + (size[0] // 2) - (self._button_image.get_height() // 2),
                ),
            )
        else:
            pygame.draw.rect(
                surface,
                (0, 0, 0),
                (*pos, *size),
            )
        return
