
import pygame as pg

from pg_widgets.utils.Primitives import roundedRect
from .UIElement import UIElement

class ProgressBar(UIElement):
    def __init__(self, pos, size = (1.0, 1.0), *, current_progress: float = 0.0):
        super().__init__(pos, size)
        self._current_progress = min(1.0, max(0.03, current_progress))

    def setValue(self, value):
        self._current_progress = min(1.0, max(0.03, value))
        self._updateSurf = True

    def getValue(self):
        return self._current_progress

    def render(self, bgColor = (0, 0, 0)):
        if (self._updateSurfBase):
            self._updateSurfBase = False

            x = self._parentSize[0] * self._size[0]
            y = self._parentSize[1] * self._size[1]

            self._surfBase = pg.Surface((x, y))
            self._surfBase.fill(bgColor)

            rOut = pg.Rect(0, 0, x, y)
            roundedRect(self._surfBase, rOut, 10, (200, 200, 200))

        if (self._updateSurf):
            self._updateSurf = False
            self._surf = self._surfBase.copy()

            offset = 2
            length = (self._parentSize[0] * self._size[0] - 2 * offset) * self._current_progress
            rInn = pg.Rect(1 * offset, 1 * offset, length, self._parentSize[1] * self._size[1] - 2 * offset)
            roundedRect(self._surf, rInn, 10, (0, 200, 0))

        return self._surf