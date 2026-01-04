
from .UIGroup import UIGroup

class Border(UIGroup):
    def __init__(self, pos, size = (1.0, 1.0), *, borderX: float = None, borderY: float = None):
        super().__init__(pos, size)
        self._uiElements = {}

        self.__borderX: float = borderX
        self.__borderY: float = borderY

    def getValue(self):
        return self._uiElements["main"].getValue()

    def __getattr__(self, name):
        return getattr(self._uiElements["main"], name)

    def changeSize(self, newSize):
        self._parentSize = newSize

        x = newSize[0] * self._size[0]
        y = newSize[1] * self._size[1]

        bx = self.__borderX / x
        by = self.__borderY / y

        self["main"].setPos(bx, by)
        self["main"].setSize((1.0 - 2 * bx, 1.0 - 2 * by))
        self["main"].changeSize((x, y))
