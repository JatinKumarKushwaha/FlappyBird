import pygame


# Draw some text at position (x, y)
def draw_text(x, y, text, font, color, surface, placeRect="center"):
    textobj = font.render(text, False, color)
    textrect = textobj.get_rect()

    # Placemenet of the textrect
    # Possilbe values
    # ["top", "left", "bottom", "right", "topleft", "bottomleft", "topright", "bottomright", "midtop", "midleft", "midbottom", "midright", "center", "centerx", "centery"]:
    if placeRect == "top":
        textrect.top = (x, y)
    elif placeRect == "left":
        textrect.left = (x, y)
    elif placeRect == "bottom":
        textrect.bottom = (x, y)
    elif placeRect == "right":
        textrect.right = (x, y)
    elif placeRect == "topleft":
        textrect.topleft = (x, y)
    elif placeRect == "bottomleft":
        textrect.bottomleft = (x, y)
    elif placeRect == "topright":
        textrect.topright = (x, y)
    elif placeRect == "bottomright":
        textrect.bottomright = (x, y)
    elif placeRect == "midtop":
        textrect.midtop = (x, y)
    elif placeRect == "midleft":
        textrect.midleft = (x, y)
    elif placeRect == "midbottom":
        textrect.midbottom = (x, y)
    elif placeRect == "midright":
        textrect.midright = (x, y)
    elif placeRect == "center":
        textrect.center = (x, y)
    elif placeRect == "centerx":
        textrect.centerx = (x, y)
    elif placeRect == "centery":
        textrect.centery = (x, y)
    else:
        textrect.center = (x, y)

    surface.blit(textobj, textrect)
