import time
import pygame as pg

from .Primitives import roundedRect, circle
from .UIElement import UIElement

class UIGroup:
    def __init__(self, pos, size = (1.0, 1.0)):
        self._pos = pos
        self._parentSize = None
        self._size = size

        self._uiElements = {}
        self._secondaryElements = []

        self._outline = False
        self._outlineColor = None

    def toggleOutline(self, color: tuple[int, int, int] = None):
        self._outline = not self._outline
        self._outlineColor = color

    def __getitem__(self, item):
        return self._uiElements[item]

    def __setitem__(self, key, value):
        self._uiElements[key] = value

    def getSize(self):
        return (
            self._parentSize[0] * self._size[0],
            self._parentSize[1] * self._size[1]
        )

    def changeSize(self, newSize):
        self._parentSize = newSize

        x = self._parentSize[0] * self._size[0]
        y = self._parentSize[1] * self._size[1]

        for (id, element) in self._uiElements.items():
            element.changeSize((x, y))

    def getPos(self):
        x = self._parentSize[0] * self._pos[0]
        y = self._parentSize[1] * self._pos[1]
        return (x, y)

    def getValue(self):
        out = {}
        for (k, v) in self._uiElements.items():
            out[k] = v.getValue()
        return out

    def update(self, mousePress, mousePos):
        for (id, element) in self._uiElements.items():
            x, y = mousePos
            dx, dy = self._parentSize[0] * self._pos[0], self._parentSize[1] * self._pos[1]
            element.update(mousePress, (x - dx, y - dy))

    def render(self, bgColor, debug: bool = False):
        x = self._parentSize[0] * self._size[0]
        y = self._parentSize[1] * self._size[1]
        surf = pg.Surface((x, y))
        surf.fill(bgColor)

        if self._outline:
            if (self._outlineColor is None):
                r, g, b = bgColor
                bgColor = (max(r - 10, 0), max(g - 10, 0), max(b - 10, 0))
            else:
                bgColor = self._outlineColor

        for (k, v) in self._uiElements.items():
            surf.blit(v.render(bgColor), v.getPos())

            for element in v._secondaryElements:
                x, y = element.getPos()
                dx, dy = v.getPos()
                surf.blit(element.render(bgColor), (x + dx, y + dy))

        return surf