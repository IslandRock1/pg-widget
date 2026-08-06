
from enum import Enum
from time import perf_counter

import pygame
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

    def __init__(self, pos, size = (1.0, 1.0)):
        super().__init__(pos, size)

        self._textSize = None
        self._text = ""

        self._timeOfUnderscoreSwitch = perf_counter()
        self._addUnderScore = False

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

    def updateKeyboard(self, event: pg.event.Event):
        if not self._isSelected: return
        if (event.type != pg.KEYDOWN): return
        self._updateSurf = True

        if event.key == pg.K_RETURN:
            self._isSelected = False
            return

        if (event.mod & pg.KMOD_NONE) or (event.mod & pg.KMOD_NUM) or (event.mod & pg.KMOD_SHIFT) or (event.mod & pg.KMOD_ALT):
            if (event.key == pg.K_BACKSPACE):
                if (len(self._text) > 0):
                    self._text = self._text[:-1]

            elif (event.key == pg.K_SPACE):
                self._text += " "

            else:
                if (event.key in [pg.K_LSHIFT, pg.K_LALT, pg.K_RALT, pg.K_LCTRL, pg.K_RCTRL]): return

                if (event.key == pg.K_PLUS) and (event.mod & pg.KMOD_SHIFT):
                    self._text += "?"
                    return

                if (event.key == pg.K_PERIOD) and (event.mod & pg.KMOD_SHIFT):
                    self._text += ":"
                    return

                out = pg.key.name(event.key)
                if (event.mod & pg.KMOD_SHIFT):
                    if out.isalpha():
                        out = out.upper()
                    elif out.isnumeric():
                        out = '=!"#¤%&/()'[int(out)]

                if (event.mod & pg.KMOD_ALT):
                    if out.isnumeric():
                        out = " @£$€ {[]}"[int(out)]

                self._text += out
        else:
            if (event.mod & pg.KMOD_CTRL) and (event.key == pg.K_BACKSPACE):
                self._text = ""

            else:
                self._text = "Invalid?"

    def render(self, bgColor = (0, 0, 0)):
        if (self._isSelected):
            tNow = perf_counter()
            if (tNow - self._timeOfUnderscoreSwitch) > 0.3:
                self._timeOfUnderscoreSwitch = tNow

                self._addUnderScore = not self._addUnderScore
                self._updateSurf = True

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
            textSurf = self._getFont(self._textSize).render(self._text + "_" * self._addUnderScore * self._isSelected, True, self._getColor("textColor"), self._colors["textBgColor"])
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