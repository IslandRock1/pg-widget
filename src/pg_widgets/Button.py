
from .basics.TextBox import TextBox

class Button(TextBox):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self._callbackFunction = lambda x: None
        self._callbackVariable = None

        self._isSelectable = False

    def setFunction(self, callbackFunction):
        self._callbackFunction = callbackFunction

    def setVariable(self, callbackVariable):
        self._callbackVariable = callbackVariable

    def _leftClick(self, mousePress, mousePos):
        super()._leftClick(mousePress, mousePos)
        self._callbackFunction(self._callbackVariable)