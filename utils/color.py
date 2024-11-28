import pygame


def tint(surf, tint_color):
    tinted_image = surf.copy()
    tint_surface = pygame.Surface(tinted_image.get_size()).convert_alpha()
    tint_surface.fill(tint_color)
    tinted_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    return tinted_image
