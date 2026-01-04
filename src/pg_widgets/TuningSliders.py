
from .basics.UIGroup import UIGroup
from .basics.TextBox import TextBox
from .basics.Slider import Slider

class TuningSliders(UIGroup):
    def __init__(self, pos, size = (1.0, 1.0), *, labels: list[str], lower_bounds: list[float] = None, upper_bounds: list[float] = None, current_values: list[float] = None):
        super().__init__(pos, size)
        self._labels = labels

        sizeY = 0.1

        for i, label in enumerate(labels):
            posX = i / len(labels)
            sizeX = (1 / len(labels))

            nameL = f"text{label}"
            self[nameL] = TextBox.inBorder((posX, 0), (sizeX, sizeY), borderX=3, borderY=3)

            nameV = f"value{label}"
            self[nameV] = TextBox.inBorder((posX, sizeY), (sizeX, sizeY), borderX=3, borderY=3)

            nameS = f"slider{label}"
            self[nameS] = Slider.inBorder((posX, 2 * sizeY), (sizeX, 1 - 2 * sizeY), borderX=3, borderY=3)

            if (current_values is not None) and (current_values[i] is not None):
                self[nameL].setText(f"{label}:")
                self[nameS].setValue(f"{current_values[i]}")
                self[nameS].changeValues(lower_bounds[i], upper_bounds[i], current_values[i])
            elif (lower_bounds is not None) and (lower_bounds[i] is not None):
                self[nameL].setText(f"{label}: {lower_bounds[i]}")
                self[nameS].changeValues(lower_bounds[i], upper_bounds[i], lower_bounds[i])
            else:
                self[nameL].setText(f"{label}: 0.0")

    def getValue(self):
        out = []
        for label in self._labels:
            out.append(self[f"slider{label}"].getValue())
        return out

    def update(self, mousePress, mousePos):
        super().update(mousePress, mousePos)

        for (l, v) in zip(self._labels, self.getValue()):
            self[f"text{l}"].setText(f"{l}:")
            self[f"value{l}"].setText(f"{v:.2f}")