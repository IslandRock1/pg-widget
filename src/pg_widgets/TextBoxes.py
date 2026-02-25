
from .basics.UIGroup import UIGroup
from .basics.TextBox import TextBox

class TextBoxes(UIGroup):
    def __init__(self, pos, size, *, labels):
        super().__init__(pos, size)

        sizeY = 1 / len(labels)
        for i, text in enumerate(labels):
            posY = i * sizeY

            name = f"text{i}"
            self[name] = TextBox((0, posY), (1.0, sizeY))
            self[name].setText(text)

    def setText(self, text, ix):
        self[f"text{ix}"].setText(text)

    def setTexts(self, texts):
        for ix, text in enumerate(texts):
            self[f"text{ix}"].setText(text)