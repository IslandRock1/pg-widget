
import pygame as pg

from .basics.UIElement import UIElement
from .basics.TextBox import TextBox
from .basics.UIGroup import UIGroup

class Tab(UIGroup):
    def __init__(self, pos, size = (1.0, 1.0), uiElements: list[UIElement] = []):
        super().__init__(pos, size)
        self._numTabs = len(uiElements)

        self._uiGroups: list[UIGroup] = uiElements
        self._activeGroup = [0]

        xSize = 0.05
        ySize = 0.05

        xPosBase = 1.0 - xSize * self._numTabs
        yPosBase = 1.0 - ySize
        for i in range(self._numTabs):

            label = str(i + 1)

            self[f"button{label}"]: UIElement = TextBox.inBorder((xPosBase + xSize * i, yPosBase), (xSize, ySize))
            self[f"button{label}"].setText(label)

            def f(activeGroup, idx = i):
                activeGroup[0] = idx

            self[f"button{label}"].overrideOnLeftClick(f, self._activeGroup)

    def __contains__(self, key):
        # check current level first
        if key in self._uiGroups:
            return True

        # recursively check nested UIGroup
        for elem in self._uiGroups:
            if isinstance(elem, UIGroup) and key in elem:
                return True

        return False

    def __getitem__(self, item):
        if (item.startswith("tab")):
            tabNr = int(item[3:]) - 1
            return self._uiGroups[tabNr]
        elif (item in self._uiElements):
            return self._uiElements[item]
        elif (item in self._uiGroups):
            return self._uiGroups[item]
        else:
            for v in self._uiGroups:
                if (item in v):
                    return v[item]

        raise KeyError(f"{item} not in UIGroup. I contain {self._uiElements} and {self._uiGroups}")

    def __setitem__(self, key, value):
        self._uiElements[key] = value

    def changeSize(self, newSize):
        super().changeSize(newSize)
        for i in range(self._numTabs):
            self._uiGroups[i].changeSize(self.getSize())

    def getActiveTab(self):
        return self._activeGroup[0]

    def update(self, mousePress, mousePos):
        super().update(mousePress, mousePos)
        self._uiGroups[self._activeGroup[0]].update(mousePress, mousePos)

    def render(self, bgColor, debug: bool = False):
        x = self._parentSize[0] * self._size[0]
        y = self._parentSize[1] * self._size[1]
        surf = pg.Surface((x, y))
        surf.fill(bgColor)

        v = self._uiGroups[self._activeGroup[0]]
        surf.blit(v.render(bgColor), v.getPos())

        for (k, v) in self._uiElements.items():
            if (k == f"button{self._activeGroup[0] + 1}"):
                v.setColor("textBgColor", (0, 0, 100))
            else:
                v.setColor("textBgColor", (0, 0, 0))

            surf.blit(v.render(bgColor), v.getPos())

            for element in v._secondaryElements:
                x, y = element.getPos()
                dx, dy = v.getPos()
                surf.blit(element.render(bgColor), (x + dx, y + dy))

        return surf