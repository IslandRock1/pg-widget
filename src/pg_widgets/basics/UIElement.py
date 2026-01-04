
from random import randint
import pygame as pg

class UIElement:
    def __init__(self, pos, size = (1.0, 1.0)):
        if not pg.get_init(): pg.init()
        if (not pg.font.get_init()): pg.font.init()

        self._pos: tuple[float, float] = pos
        self._parentSize: tuple[float, float] = None
        self._size: tuple[float, float] = size

        self._surf = None
        self._surfBase = None
        self._updateSurf = True
        self._updateSurfBase = True

        self._secondaryElements: list[type(UIElement)] = []
        self._fonts: dict[int, pg.font.Font] = {}

        self._isLeftClick: bool = False
        self._isRightClick: bool = False
        self._isPress: bool = False

        self._leftPressShadow = False
        self._rightPressShadow = False

        self._colors = {
            "bgColor": (200, 200, 200),
            "textColor": (255, 0, 128)
        }

    @classmethod
    def inBorder(cls, pos, size = (1.0, 1.0), *, borderX: float = 5.0, borderY: float = 5.0):
        from .Border import Border
        b = Border(pos, size, borderX=borderX, borderY=borderY)

        b["main"] = cls((0, 0), (0, 0))
        return b

    def setValue(self, val):
        pass

    def getValue(self):
        pass

    def setPos(self, x, y):
        self._pos = (x, y)

    def getPos(self):
        x = self._parentSize[0] * self._pos[0]
        y = self._parentSize[1] * self._pos[1]

        return (x, y)

    def getSize(self):
        return (
            self._parentSize[0] * self._size[0],
            self._parentSize[1] * self._size[1]
        )

    def changeSize(self, newSize):
        self._parentSize = newSize

        self._updateSurfBase = True
        self._updateSurf = True

    def setSize(self, size):
        self._size = size

    def _getFont(self, textSize):
        textSize = int(textSize)
        if (textSize not in self._fonts):
            self._fonts[textSize] = pg.font.SysFont("Arial", textSize)
        return self._fonts[textSize]

    def setColor(self, name, value):
        self._colors[name] = value
        self._updateSurfBase = True
        self._updateSurf = True

    def _getColor(self, name, default = None):
        if (name not in self._colors):
            if (default is not None):
                self._colors[name] = default
            else:
                self._colors[name] = [randint(0, 255), randint(0, 255), randint(0, 255)]

        return self._colors[name]

    def _leftClick(self, mousePress, mousePos):
        pass

    def _rightClick(self, mousePress, mousePos):
        pass

    def _onPress(self, mousePress, mousePos):
        pass

    def _addSecondaryElement(self):
        pass

    def _getInfoFromSecondary(self):
        pass

    def _collision(self, x, y):
        px, py = self.getPos()
        dx, dy = self.getSize()

        if (x < px) or (y < py): return False
        if (x > px + dx) or (y > py + dy): return False
        return True

    def update(self, mousePress: tuple[bool, bool, bool], mousePos: tuple[float, float], debug: bool = False, depth: int = 0):
        self._getInfoFromSecondary()

        notPress = not any(mousePress)
        collisions = [self._collision(mousePos[0], mousePos[1])]
        for secondary in self._secondaryElements:
            x, y = mousePos
            dx, dy = self.getPos()

            collisions.append(secondary._collision((x - dx), (y - dy)))

        notCollide = not any(collisions)

        dx, dy = self.getPos()
        for secondary in self._secondaryElements:
            x, y = mousePos
            secondary.update(mousePress, (x - dx, y - dy), depth = depth + 1)

        secondaryPress = [secondary._isPress for secondary in self._secondaryElements]
        if (any(mousePress)) and (not self._isPress) and (not any(secondaryPress)):
            self._secondaryElements = []

        if (notCollide):
            self._leftPressShadow = mousePress[0]
            self._rightPressShadow = mousePress[2]
            return

        onlyMainCollide = collisions[0] and not any(collisions[1:])
        if (self._leftPressShadow and not mousePress[0]) and (onlyMainCollide):
            self._isLeftClick = True
            self._leftClick(mousePress, mousePos)
        else: self._isLeftClick = False

        if (self._rightPressShadow and not mousePress[2]) and (onlyMainCollide):
            self._isRightClick = True
            self._rightClick(mousePress, mousePos)
        else: self._isRightClick = False

        if any(mousePress) and (onlyMainCollide):
            self._isPress = True
            self._onPress(mousePress, mousePos)
        else: self._isPress = False

        if (self._isRightClick) and (len(self._secondaryElements) == 0) and (depth == 0):
            self._addSecondaryElement()

        self._leftPressShadow = mousePress[0]
        self._rightPressShadow = mousePress[2]