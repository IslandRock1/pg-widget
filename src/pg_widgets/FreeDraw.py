
import pygame as pg

from .basics.UIElement import UIElement

class FreeDraw(UIElement):
    def __init__(self, pos, size):
        super().__init__(pos, size)

    def __unNormalize(self, pos):
        x, y = self.getSize()
        return (pos[0] * x, pos[1] * y)

    def fill(self, color = None):
        if color is None: color = self._getColor("bgColor")
        self._surf.fill(color)

    def circle(self, pos, radius, color):
        pos = self.__unNormalize(pos)

        x, y = self.getSize()
        radius = radius * min(x, y)
        pg.draw.circle(self._surf, color, pos, radius, 1)

    def line(self, start, end, width, color):
        start = self.__unNormalize(start)
        end = self.__unNormalize(end)
        pg.draw.line(self._surf, color, start, end, width)

    def __lineRaw(self, start, end, width, color):
        pg.draw.line(self._surf, color, start, end, width)

    def arrow(self, start, end, width, color):
        start = self.__unNormalize(start)
        end = self.__unNormalize(end)
        self.__lineRaw(start, end, width, color)

        xs, ys = start
        xe, ye = end
        alongX = xe - xs
        alongY = ye - ys

        midX = xs + alongX * 0.9
        midY = ys + alongY * 0.9
        mid = (midX, midY)

        leftPoint = (midX + alongY * 0.05, midY - alongX * 0.05)
        rightPoint = (midX - alongY * 0.05, midY + alongX * 0.05)

        self.__lineRaw(mid, leftPoint, width, color)
        self.__lineRaw(mid, rightPoint, width, color)

        self.__lineRaw(leftPoint, end, width, color)
        self.__lineRaw(rightPoint, end, width, color)

    def text(self, pos, text, size, color, bgColor = None):
        pos = self.__unNormalize(pos)

        if bgColor is None: bgColor = self._getColor("bgColor")
        renderedText = self._getFont(size).render(text, True, color, bgColor)
        tw, th = renderedText.get_width(), renderedText.get_height()
        self._surf.blit(renderedText, (pos[0] - tw / 2, pos[1] - th / 2))


    def render(self, bgColor = (0, 0, 0)):
        if (self._updateSurfBase):
            self._updateSurfBase = False

            x, y = self.getSize()
            self._surfBase = pg.Surface((x, y))
            self._surfBase.fill((bgColor))

        if (self._updateSurf):
            self._updateSurf = False

            self._surf = self._surfBase.copy()

        return self._surf