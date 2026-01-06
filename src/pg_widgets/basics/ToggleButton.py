import pygame as pg

from pg_widgets.utils.Primitives import circle, roundedRect
from .UIElement import UIElement

class ToggleButton(UIElement):
    def __init__(self, pos, size, *, state: bool = False):
        super().__init__(pos, size)

        self.dir = None
        self.bgColor = (200, 210, 220)
        self.slidyCircleColor = (0, 210, 220)
        self._state = state

    def setValue(self, val):
        self._state = val
        self._updateSurf = True

    def getValue(self):
        return self._state

    def changeSize(self, newSize):
        super().changeSize(newSize)
        self.dir = (self._parentSize[0] * self._size[0] > self._parentSize[1] * self._size[1])

    def _leftClick(self, mousePress, mousePos):
        self._state = not self._state
        self._updateSurf = True

    def render(self, bgColor = (0, 0, 0)):
        if (self._updateSurfBase):
            self._updateSurfBase = False

            size = self.getSize()

            self._surfBase = pg.Surface(size)
            self._surfBase.fill(bgColor)

            rect = pg.Rect(0, 0, size[0], size[1])
            roundedRect(self._surfBase, rect, int(min(size[0], size[1]) // 2 - 1), self.bgColor)

        if (self._updateSurf):
            self._updateSurf = False
            self._surf = self._surfBase.copy()

            size = self.getSize()

            if (self.dir):
                circleRadius = int(size[1] * 0.4)
                circleX = circleRadius + int(size[0] * 0.02)
                if (self._state): circleX = size[0] - circleX
                circle(self._surf, int(circleX), int(size[1] // 2), circleRadius, self.slidyCircleColor)
            else:
                circleRadius = int(size[0] * 0.4)
                circleX = circleRadius + int(size[1] * 0.02)
                if (self._state): circleX = size[1] - circleX
                circle(self._surf, int(size[0] // 2), int(circleX), circleRadius, self.slidyCircleColor)

        return self._surf