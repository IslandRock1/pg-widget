
import pygame as pg

from pg_widgets.utils.Primitives import roundedRect
from .UIElement import UIElement

class Plot(UIElement):
    def __init__(self, pos, size = (1.0, 1.0)):
        super().__init__(pos, size)

        self._x_values = [[0.0]]
        self._y_values = [[0.0]]

        self._offset = None
        self._text_x_ratio = 0.05
        self._text_y_ratio = 0.05
        self._fontSize = 15

        self._x_low: float = None
        self._dx: float = None
        self._y_low: float = None
        self._dy: float = None

        self._x_low_user: float = None
        self._dx_user: float = None
        self._y_low_user: float = None
        self._dy_user: float = None

        self._min_px: int = None
        self._max_px: int = None
        self._min_py: int = None
        self._max_py: int = None

        self._title: str = ""
        self._x_label: str = ""
        self._y_label: str = ""

    def changeSize(self, newSize):
        super().changeSize(newSize)

        self._offset = min(self._size) * min(self._parentSize) * 0.1
        self._updateOffset()

    def _updateOffset(self):
        self._min_px = self._offset * 2
        self._min_py = self._offset
        self._max_px = (self._parentSize[0] * self._size[0] - self._offset)
        self._max_py = (self._parentSize[1] * self._size[1] - self._offset)
        self._computeParams()

    def setTitle(self, title: str):
        self._title = title
        self._updateSurfBase = True
        self._updateSurf = True

    def setXLabel(self, x_label: str):
        self._x_label = x_label
        self._updateSurf = True
        self._updateSurf = True

    def setYLabel(self, y_label: str):
        self._y_label = y_label
        self._updateSurf = True
        self._updateSurf = True

    def setBounds(self, x_low: float = None, x_high: float = None, y_low: float = None, y_high: float = None):
        if (x_low is not None):
            self._x_low_user = x_low
        if (x_high is not None) and (x_low is not None):
            self._dx_user = x_high - x_low

        if (y_low is not None):
            self._y_low_user = y_low
        if (y_high is not None) and (y_low is not None):
            self._dy_user = y_high - y_low

        self._computeParams()
        self._updateSurf = True
        self._updateSurf = True

    def setValue(self, x_values: list[float], y_values: list[float], plotIx: int = 0, maxLength: int = None, debug: bool = False):
        x_values = [x for x in x_values]
        y_values = [y for y in y_values]

        while (len(self._x_values) <= plotIx):
            self._x_values.append([0.0])
            self._y_values.append([0.0])

        if (len(x_values) != 0): self._x_values[plotIx] = x_values
        else: self._x_values[plotIx] = [0.0]

        if (len(y_values) != 0): self._y_values[plotIx] = y_values
        else: self._y_values[plotIx] = [0.0]

        if (maxLength is not None):
            while (len(self._x_values[plotIx]) > maxLength):
                self._x_values[plotIx].pop(0)
                self._y_values[plotIx].pop(0)

        self._computeParams()
        self._updateSurf = True

    def addValue(self, x, y, plotIx: int = 0, maxLength: int = None):
        self._x_values[plotIx].append(x)
        self._y_values[plotIx].append(y)

        if (maxLength is not None):
            while (len(self._x_values[plotIx]) > maxLength):
                self._x_values[plotIx].pop(0)
                self._y_values[plotIx].pop(0)

        self._computeParams()
        self._updateSurf = True

    def _computeParams(self, debug: bool = False):
        if (self._x_low_user is None):
            self._x_low = min([min(v) for v in self._x_values])
        else:
            self._x_low = self._x_low_user

        if (self._dx_user is None):
            self._dx = max([max(v) for v in self._x_values]) - self._x_low
        else:
            self._dx = self._dx_user

        if (self._y_low_user is None):
            self._y_low = min([min(v) for v in self._y_values])
        else:
            self._y_low = self._y_low_user

        if (self._dy_user is None):
            self._dy = max([max(v) for v in self._y_values]) - self._y_low
        else:
            self._dy = self._dy_user

    def _getPixelPos(self):

        points = []
        for plotIx in range(len(self._x_values)):
            out = []
            for (x, y) in zip(self._x_values[plotIx], self._y_values[plotIx]):

                if (self._dx != 0):
                    x_ratio = (x - self._x_low) / self._dx
                else: x_ratio = 0.0

                if (self._dy != 0):
                    y_ratio = (y - self._y_low) / self._dy
                else: y_ratio = 0.0

                x_pos = self._min_px + x_ratio * (self._max_px - self._min_px)
                y_pos = self._max_py - y_ratio * (self._max_py - self._min_py)

                out.append((int(x_pos), int(y_pos)))
            points.append(out)
        return points

    def _textItRatio(self, mainSurf, text, xRatio, yRatio, fontSize: int = 20, rotate: bool = False):

        tCol = self._getColor("textColor")
        bgColor = self._getColor("bgColor")

        surf = self._getFont(fontSize).render(text, True, tCol, bgColor)
        w, h = self._parentSize[0] * self._size[0] * xRatio, self._parentSize[1] * self._size[1] * yRatio

        wText, hText = surf.get_rect().size
        if (rotate): wText, hText = hText, wText
        dest = (w - wText // 2, h - hText // 2)

        if (rotate): surf = pg.transform.rotate(surf, 90)
        mainSurf.blit(surf, dest)

    def _textItAbsolute(self, mainSurf, text, x, y, fontSize: int = 20, rotate: bool = False):

        tCol = self._getColor("textColor")
        bgColor = self._getColor("bgColor")

        surf = self._getFont(fontSize).render(text, True, tCol, bgColor)

        wText, hText = surf.get_rect().size
        if (rotate): wText, hText = hText, wText
        dest = (x - wText // 2, y - hText // 2)

        if (rotate): surf = pg.transform.rotate(surf, 90)
        mainSurf.blit(surf, dest)

    def _formatN(self, x, sig=3):
        # Created by ChatGPT (fixed by me lol)
        if x == 0:
            return "0"
        abs_x = abs(x)
        if 1e-3 <= abs_x < 1e4:
            out = f"{x:.{sig}g}"
        else:
            out = f"{x:.{sig}e}"

        if "+" in out:
            out = out.replace("+", "")

        if "e" in out:
            pre, aft = out.split("e")
            while aft[0] == "0": aft = aft[1:]
            out = f"{pre}e{aft}"

        return out

    def render(self, bgColor = (0, 0, 0)):
        if (self._updateSurfBase):
            self._updateSurfBase = False

            x = self._parentSize[0] * self._size[0]
            y = self._parentSize[1] * self._size[1]

            self._surfBase = pg.Surface((x, y))
            self._surfBase.fill(bgColor)

            roundedRect(self._surfBase, pg.Rect(0, 0, x, y), 20, self._getColor("bgColor"))

            outerPoints = [
                (self._min_px, self._min_py),
                (self._max_px, self._min_py),
                (self._max_px, self._max_py),
                (self._min_px, self._max_py)
            ]
            pg.draw.aalines(self._surfBase, (0,0,0), True, outerPoints)

            midX = (self._min_px + self._max_px) / 2
            midY = (self._min_py + self._max_py) / 2

            self._textItAbsolute(self._surfBase, self._title, midX, self._min_py // 2)
            self._textItAbsolute(self._surfBase, self._x_label, midX, self._max_py + self._min_py // 2)
            self._textItAbsolute(self._surfBase, self._y_label, self._min_px // 2, midY, rotate=True)


        if (self._updateSurf):
            self._updateSurf = False

            self._surf = self._surfBase.copy()
            pixelPos = self._getPixelPos()
            for points in pixelPos:
                if (len(points) > 2):
                    pg.draw.aalines(self._surf, (0,0,0), False, points)

            self._textItAbsolute(self._surf, str(self._x_low), self._min_px, self._max_py + self._min_py // 2)
            self._textItAbsolute(self._surf, str(self._x_low + self._dx), self._max_px, self._max_py + self._min_py // 2)

            self._textItAbsolute(self._surf, self._formatN(self._y_low), self._min_px // 2, self._max_py)
            self._textItAbsolute(self._surf, self._formatN(self._y_low + self._dy), self._min_px // 2, self._min_py)

        return self._surf