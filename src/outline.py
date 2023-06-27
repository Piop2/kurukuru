import pygame


def perfect_outline(
    surface: pygame.Surface, img: pygame.Surface, loc: list[int | float]
):
    mask = pygame.mask.from_surface(img)
    mask_surf_white = mask.to_surface()
    mask_surf_white.set_colorkey((0, 0, 0))

    surface.blit(mask_surf_white, (loc[0] - 5, loc[1]))
    surface.blit(mask_surf_white, (loc[0] + 5, loc[1]))
    surface.blit(mask_surf_white, (loc[0], loc[1] - 5))
    surface.blit(mask_surf_white, (loc[0], loc[1] + 5))
    return
