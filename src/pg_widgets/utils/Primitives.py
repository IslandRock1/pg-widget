
import pygame as pg
from pygame import gfxdraw

def circle(surf, x, y, radius, color):
    gfxdraw.aacircle(surf, x, y, radius, color)
    gfxdraw.filled_circle(surf, x, y, radius, color)

def roundedRect(surf: pg.Surface, rect: pg.Rect, borderRadius: int, color: tuple[int, int, int]):

    circle(surf, rect.left + borderRadius, rect.top + borderRadius, borderRadius, color)
    circle(surf, rect.left + rect.width - borderRadius - 1, rect.top + borderRadius, borderRadius, color)
    circle(surf, rect.left + borderRadius, rect.top + rect.height - borderRadius - 1, borderRadius, color)
    circle(surf, rect.left + rect.width - borderRadius - 1, rect.top + rect.height - borderRadius - 1, borderRadius,color)

    slimRect = pg.Rect(rect.left + borderRadius, rect.top, rect.width - 2 * borderRadius, rect.height)
    gfxdraw.box(surf, slimRect, color)

    wideRect = pg.Rect(rect.left, rect.top + borderRadius, rect.width, rect.height - 2 * borderRadius)
    gfxdraw.box(surf, wideRect, color)