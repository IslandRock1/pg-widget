
import pygame as pg

from .Primitives import circle, roundedRect
from .UIElement import UIElement

class TextBox(UIElement):
    def __init__(self, pos, size = (1.0, 1.0), *, text = ""):
        super().__init__(pos, size)

        self._textSize = None
        self._text = text

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

            self._surf.blit(textSurf, ((w - wText) // 2, (h - hText) // 2))

        return self._surf