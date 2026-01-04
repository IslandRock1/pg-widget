
from colorsys import hsv_to_rgb

from .basics.UIGroup import UIGroup
from .basics.TextBox import TextBox
from .basics.Slider import Slider

class ColorPicker(UIGroup):
    def __init__(self, pos, size):
        super().__init__(pos, size)

        self._HSV = [0, 0, 0]
        self._RGB = [0, 0, 0]
        third = 0.33

        for (i, name) in enumerate(["Hue", "Sat", "Val"]):
            self[f"text{name}"] = TextBox.inBorder((i * third, 0), (third, 0.2))
            self[f"text{name}"].setText(name)

            self[f"slider{name}"] = Slider.inBorder((i * third, 0.2), (third, 0.8))
            self[f"slider{name}"].setValue(1.0)

    def getValue(self):
        return self._RGB

    def update(self, mousePress, mousePos):
        super().update(mousePress, mousePos)

        self._HSV[0] = self["sliderHue"].getValue()
        self._HSV[1] = self["sliderSat"].getValue()
        self._HSV[2] = self["sliderVal"].getValue()

        h, s, v = self._HSV
        self._RGB = [int(x * 255) for x in hsv_to_rgb(h, s, v)]

        for (i, name) in enumerate(["Hue", "Sat", "Val"]):
            self[f"text{name}"].setColor("textColor", self._RGB)