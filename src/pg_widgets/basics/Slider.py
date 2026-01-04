
import pygame as pg
from pygame import gfxdraw

from .Primitives import circle, roundedRect
from .UIElement import UIElement

def bound(value, range0, range1):
    minV, maxV = min(range0, range1), max(range0, range1)
    return min(maxV, max(minV, value))

class Slider(UIElement):
    def __init__(self, pos, size, *, firstVal = 0.0, secondVal = 1.0, currentVal = 0.0):
        super().__init__(pos, size)

        self._firstVal = firstVal
        self._secondVal = secondVal
        self._currentVal = currentVal

        self._dir = None
        self._buffer = 0.02

        self._bgColor = (200, 210, 220)
        self._lineColor = (10, 10, 10)
        self._slidyBoxColor = (0, 210, 220)

        self._mainRadius = 10

    def changeValues(self, firstValue, secondValue, currentValue = None):

        if (currentValue is None):
            if (self._firstVal == self._secondVal):
                prevRatio = 0.5
            else:
                minV, maxV = min(self._firstVal, self._secondVal), max(self._firstVal, self._secondVal)
                ratio = (self._currentVal - minV) / (maxV - minV)
                prevRatio = ratio if (self._firstVal < self._secondVal) else 1.0 - ratio

        self._firstVal = firstValue
        self._secondVal = secondValue

        if (currentValue is None):
            self._currentVal = prevRatio * (self._secondVal - self._firstVal) + self._firstVal
        else:
            self._currentVal = currentValue
        self._currentVal = bound(self._currentVal, self._firstVal, self._secondVal)
        self._updateSurf = True

    def setValue(self, value):
        self._currentVal = value
        self._updateSurf = True

    def getValue(self):
        return self._currentVal

    def changeSize(self, newSize):
        super().changeSize(newSize)
        self._dir = (self._parentSize[0] * self._size[0] > self._parentSize[1] * self._size[1])

    def _onPress(self, mousePress, mousePos):
        super()._onPress(mousePress, mousePos)

        if (not mousePress[0]):
            return

        x = self._parentSize[0] * self._size[0]
        y = self._parentSize[1] * self._size[1]

        mousePos = (
            mousePos[0] - self._parentSize[0] * self._pos[0],
            mousePos[1] - self._parentSize[1] * self._pos[1]
        )

        if (self._dir):
            # Horizontal, x axis in focus
            mouse, _ = mousePos
            sizeIx = 0
        else:
            # Vertical, y axis in focus
            _, mouse = mousePos
            sizeIx = 1

        offset = self._buffer * self._parentSize[sizeIx] * self._size[sizeIx]

        if (mouse < offset):
            pos = offset
        elif (mouse > ((x, y)[sizeIx] - offset)):
            pos = ((x, y)[sizeIx] - offset)
        else:
            pos = mouse

        ratio = (pos - offset) / (self._parentSize[sizeIx] * self._size[sizeIx] - 2 * offset)
        self._currentVal = self._firstVal + ratio * (self._secondVal - self._firstVal)
        self._updateSurf = True

    def _getRatio(self):
        if (self._secondVal == self._firstVal):
            return 0.5
        else:
            minV, maxV = min(self._firstVal, self._secondVal), max(self._firstVal, self._secondVal)
            ratio = (self._currentVal - minV) / (maxV - minV)
            return ratio if (self._firstVal < self._secondVal) else 1.0 - ratio

    def _getRects(self):
        ratio = self._getRatio()
        sizeIx = 0 if self._dir else 1
        buffer_pixels = int(self._buffer * self._parentSize[sizeIx] * self._size[sizeIx])
        xy_pos = buffer_pixels + ratio * (self._parentSize[sizeIx] * self._size[sizeIx] - 2 * buffer_pixels - 20)

        if (self._dir):
            rectSmol = pg.Rect(xy_pos, 5, 20, self._parentSize[1] * self._size[1] - 10)
        else:
            rectSmol = pg.Rect(5, xy_pos, self._parentSize[0] * self._size[0] - 10, 20)

        return rectSmol

    def _getRectsBase(self):

        x = self._parentSize[0] * self._size[0]
        y = self._parentSize[1] * self._size[1]

        rect = pg.Rect(0, 0, x, y)

        sizeIx = 0 if self._dir else 1
        buffer_pixels = int(self._buffer * self._parentSize[sizeIx] * self._size[sizeIx])

        if (self._dir):
            rectWide = pg.Rect(buffer_pixels + 1,
                               y * 0.48,
                               x - 2 * buffer_pixels - 2,
                               y * 0.04)
        else:
            rectWide = pg.Rect(x * 0.48,
                               buffer_pixels + 1,
                               x * 0.04,
                               y - 2 * buffer_pixels - 2)

        return (rect, rectWide)

    def render(self, bgColor = (0, 0, 0)):
        if (self._updateSurfBase):
            self._updateSurfBase = False

            x = self._parentSize[0] * self._size[0]
            y = self._parentSize[1] * self._size[1]

            self._surfBase = pg.Surface((x, y))
            self._surfBase.fill(bgColor)

            rect, rectWide = self._getRectsBase()

            roundedRect(self._surfBase, rect, self._mainRadius, self._bgColor)
            roundedRect(self._surfBase, rectWide, 0, self._lineColor)

        if (self._updateSurf):
            self._updateSurf = False

            self._surf = self._surfBase.copy()
            rectSmol = self._getRects()
            roundedRect(self._surf, rectSmol, 5, self._slidyBoxColor)

        return self._surf