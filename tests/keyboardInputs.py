import pg_widgets as pw

def main():
    controlManager = pw.ControlManager()

    b = pw.Button((0.4, 0.4), (0.2, 0.2))
    controlManager["button"] = b

    t = pw.TextBox((0.4, 0.1), (0.2, 0.2))
    controlManager["textBox"] = t

    labels = ["Torque", "Velocity", "Position"]
    lower = [20000, 20000, 20000]
    upper = [1, 1, 1]
    s = pw.TuningSliders((0.0, 0.0), (0.35, 1.0), labels=labels, upper_bounds=upper, lower_bounds=lower)
    controlManager["sliders"] = s

    fpsLabel = pw.TextBox((0.8, 0.9), (0.2, 0.1))
    controlManager["fps"] = fpsLabel
    while controlManager.isRunning():

        fpsLabel.setText(f"{controlManager.getRenderTime() * 1000.0:.3f} ms | {1.0 / controlManager.getRenderTime():.2f} fps")
        controlManager.update()

    controlManager.close()

if __name__ == "__main__":
    main()