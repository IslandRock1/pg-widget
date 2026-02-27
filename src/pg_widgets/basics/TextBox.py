
from enum import Enum
from unittest import case

import pygame as pg

from pg_widgets.utils.Primitives import roundedRect
from .UIElement import UIElement

class TextBox(UIElement):
    class AlignmentHorizontal:
        LEFT = 0
        MIDDLE = 1
        RIGHT = 2

    class AlignmentVertical(Enum):
        TOP = 0
        MIDDLE = 1
        BOTTOM = 2

    def __init__(self, pos, size = (1.0, 1.0), *, text = ""):
        super().__init__(pos, size)

        self._textSize = None
        self._text = text

        self._alignmentHorizontal = self.AlignmentHorizontal.MIDDLE
        self._alignmentVertical = self.AlignmentVertical.MIDDLE

    def changeSize(self, newSize):
        super().changeSize(newSize)

        self._textSize = int(self._parentSize[1] * self._size[1] * 1.0)

    def setText(self, text: str):
        self._text = text
        self._updateSurf = True

    def getText(self):
        return self._text

    def setTextSize(self, size: int):
        self._textSize = int(size)
        self._updateSurf = True

    def setAlignment(self, *, horizontal = None, vertical = None):

        if horizontal is not None:
            self._alignmentHorizontal = horizontal
            self._updateSurf = True

        if vertical is not None:
            self._alignmentVertical = vertical
            self._updateSurf = True

    def _getInfoFromSecondary(self):
        if (len(self._secondaryElements) > 0):
            self._textSize = int(self._secondaryElements[0].getValue())
            self._updateSurf = True

    def render(self, bgColor = (0, 0, 0)):
        if (self._updateSurfBase):
            self._updateSurfBase = False

            x = self._parentSize[0] * self._size[0]
            y = self._parentSize[1] * self._size[1]

            self._surfBase = pg.Surface((x, y))
            self._surfBase.fill(bgColor)
            rect = pg.Rect(0, 0, x, y)

            if ("textBgColor" not in self._colors):
                r, g, b = bgColor
                ro, go, bo = (10, 10, 10)
                self._colors["textBgColor"] = (min(255, r + ro), min(255, g + go), min(255, b + bo))

            roundedRect(self._surfBase, rect, 10, self._colors["textBgColor"])

        if (self._updateSurf):
            self._updateSurf = False

            self._surf = self._surfBase.copy()
            textSurf = self._getFont(self._textSize).render(self._text, True, self._getColor("textColor"), self._colors["textBgColor"])
            wText, hText = textSurf.get_rect().size
            w, h = self._parentSize[0] * self._size[0], self._parentSize[1] * self._size[1]

            if (wText > w * 0.9) or (hText > h * 0.9):
                self._textSize -= 1
                self._updateSurf = True

            match self._alignmentHorizontal:
                case self.AlignmentHorizontal.LEFT:
                    posX = max(1, int(w * 0.01))
                case self.AlignmentHorizontal.MIDDLE:
                    posX = (w - wText) // 2
                case self.AlignmentHorizontal.RIGHT:
                    posX = min(w - 1, int(w * 0.99))

            match self._alignmentVertical:
                case self.AlignmentVertical.TOP:
                    posY = max(1, int(h * 0.01))
                case self.AlignmentVertical.MIDDLE:
                    posY = (h - hText) // 2
                case self.AlignmentVertical.BOTTOM:
                    posY = min(h - 1, int(h * 0.99))

            self._surf.blit(textSurf, (posX, posY))

        return self._surf