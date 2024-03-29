import pygame


class Button:
    def __init__(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        image: pygame.Surface | None = None,
    ):
        if image is not None:
            image = image.copy()

        self._pos = pos
        self._size = size
        self._image = image
        self._rect = pygame.Rect(*pos, *size)

        self._is_pushed = False
        self._is_hovered = False

        self._value = False
        return

    @property
    def value(self) -> bool:
        if self._value:
            self._value = False
            return True
        return False

    @property
    def pos(self) -> tuple[int, int]:
        return self._pos

    @property
    def size(self) -> tuple[int, int]:
        return self._size

    def update(self, mouse_pos: tuple[int, int], is_click: bool):
        if not is_click:
            if self._rect.collidepoint(mouse_pos):
                self._is_hovered = True
                if self._is_pushed:
                    self._value = not self._value
            else:
                self._is_hovered = False
            self._is_pushed = False
            return

        if self._is_hovered:
            self._is_pushed = True
            return
        return

    def render(self, surface: pygame.Surface):
        if self._is_pushed:
            color = (200, 200, 200)
        else:
            color = (255, 255, 255)

        pygame.draw.rect(surface, color, self._rect)
        pygame.draw.rect(surface, (0, 0, 0), self._rect, 2)
        return


class FloatingButton(Button):
    def __init__(
        self,
        pos: tuple[int, int],
        size: tuple[int, int],
        default_image: pygame.Surface,
        hovered_image: pygame.Surface | None = None
    ):
        super().__init__(pos, size, None)

        self._default_image = default_image
        self._hovered_image = hovered_image
        return

    @property
    def is_hovered(self) -> bool:
        return self._is_hovered

    def update(self, mouse_pos: tuple[int, int], is_click: bool):
        if not self._rect.collidepoint(mouse_pos):
            self._is_hovered = False
            return
        self._is_hovered = True

        if not is_click:
            self._value = True
        return

    def render(self, surface: pygame.Surface):
        if not self._is_hovered:
            surface.blit(
                self._default_image,
                (
                    self._pos[0]
                    + (self._size[0] // 2)
                    - (self._default_image.get_width() // 2),
                    self._pos[1]
                    + (self._size[1] // 2)
                    - (self._default_image.get_height() // 2),
                ),
            )
            return

        if self._hovered_image is not None:
            surface.blit(
                self._hovered_image,
                (
                    self._pos[0]
                    + (self._size[0] // 2)
                    - (self._hovered_image.get_width() // 2),
                    self._pos[1]
                    + (self._size[1] // 2)
                    - (self._hovered_image.get_height() // 2),
                ),
            )
        else:
            surface.blit(
                self._default_image,
                (
                    self._pos[0]
                    + (self._size[0] // 2)
                    - (self._default_image.get_width() // 2),
                    self._pos[1]
                    + (self._size[1] // 2)
                    - (self._default_image.get_height() // 2),
                ),
            )
        return
