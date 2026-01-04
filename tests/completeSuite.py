
import pg_widgets as pw
from pg_widgets import UIGroup

from random import randint

def main():
    controlManager = pw.ControlManager()

    left = UIGroup((0, 0), (0.5, 1.0))
    left["plotTop"] = pw.Plot.inBorder((0, 0), (1.0, 0.5))
    left["plotTop"].setTitle("Top Plot")
    left["plotTop"].setXLabel("X-Axis")
    left["plotTop"].setYLabel("Y-Axis")

    left["plotBot"] = pw.Plot.inBorder((0.0, 0.5), (1.0, 0.5))
    left["plotBot"].setTitle("Bot Plot")
    left["plotBot"].setXLabel("X-Axis")
    left["plotBot"].setYLabel("Y-Axis")

    controlManager["left"] = left

    right = UIGroup((0.5, 0.0), (0.5, 1.0))
    right["text"] = pw.TextBox.inBorder((0.0, 0.0), (1.0, 0.2))

    right["sliderInput"]  = pw.Slider.inBorder((0.0, 0.2), (0.5, 0.1))
    right["sliderOutput"] = pw.Slider.inBorder((0.5, 0.2), (0.5, 0.1))
    right["sliderInput"].changeValues(1.0, 0.0, 0.5)

    right["progressbar"] = pw.ProgressBar.inBorder((0.0, 0.3), (1.0, 0.1))

    bottom = UIGroup((0.0, 0.4), (1.0, 0.6))
    bottom["togglebuttonVertical"] = pw.ToggleButton.inBorder((0.0, 0.0), (0.1, 1.0))
    bottom["togglebuttonHorizontal"] = pw.ToggleButton.inBorder((0.1, 0.0), (0.5, 0.2))

    labels = ["Param 1", "Param 2", "Param 3"]
    bottom["tuningsliders"] = pw.TuningSliders((0.6, 0.0), (0.4, 1.0), labels=labels)

    bottom["colorPicker"] = pw.ColorPicker((0.1, 0.2), (0.5, 0.8))
    bottom["colorPicker"].toggleOutline((0, 0, 0))

    right["bottom"] = bottom
    controlManager["right"] = right

    plotXValues = [0]
    plotYValues = [0]

    while controlManager.isRunning():
        plotXValues.append(len(plotXValues))
        plotYValues.append(plotYValues[-1] + randint(-10, 10))
        controlManager["left"]["plotTop"].addValue(plotXValues[-1], plotYValues[-1], maxLength=1000)
        controlManager["left"]["plotBot"].setValue(plotXValues, plotYValues, maxLength=1000)

        controlManager["right"]["text"].setText(f"Render Time: {1000 * controlManager.getRenderTime():.2f} ms")
        controlManager["right"]["sliderOutput"].setValue(controlManager["right"]["sliderInput"].getValue())

        controlManager["right"]["progressbar"].setValue(controlManager.getIteration() % 1000 / 1000)

        controlManager.update()


if __name__ == "__main__":
    main()

# TODO!
# Slider changeValues does maybe not work if currentValue is None?