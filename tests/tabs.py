

import pg_widgets as pw

def main():
    controlManager = pw.ControlManager()

    tab1 = pw.UIGroup((0.0, 0.0), (1.0, 1.0))
    tab1["slider"] = pw.Slider.inBorder((0.0, 0.0), (1.0, 0.2))

    callbackVariable = [0]
    def callbackFunction(callbackVariable):
        callbackVariable[0] += 1

    tab1["button"] = pw.Button.inBorder((0.0, 0.2), (0.2, 0.2))
    tab1["button"].setText("Press me!")
    tab1["button"].setFunction(callbackFunction)
    tab1["button"].setVariable(callbackVariable)

    tab1["progressBar"] = pw.ProgressBar.inBorder((0.2, 0.2), (0.8, 0.2))

    tab2 = pw.UIGroup((0.0, 0.0), (1.0, 1.0))
    tab2["textbox"] = pw.TextBox.inBorder((0.0, 0.0), (1.0, 0.3))
    tab2["textbox"].setText("Tab 2!")

    tab2["colorPicker"] = pw.ColorPicker((0.0, 0.3), (0.5, 0.6))
    tab2["tuningSliders"] = pw.TuningSliders((0.5, 0.3), (0.5, 0.6), labels=["Tune1", "Tune2", "Tune3", "Tune4", "Tune5"])

    controlManager["tabs"] = pw.Tab((0, 0), uiElements=[tab1, tab2])

    while controlManager.isRunning():

        controlManager["tabs"]["tab1"]["progressBar"].setValue(callbackVariable[0] % 20.0 / 20.0)

        controlManager.update()


if __name__ == "__main__":
    main()