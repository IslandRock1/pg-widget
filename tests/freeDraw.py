
from time import perf_counter
import math
import pygame as pg
import pg_widgets as pw

def getTextAndPos(numMagnets):
    textDist = 0.4
    midX = 0.5
    midY = 0.5

    angle = 0.0
    currentPositions = []
    for i in range(6 * numMagnets):
        currentPositions.append((midX + textDist * math.cos(angle), midY + textDist * math.sin(angle)))
        angle -= 2 * math.pi / (6 * numMagnets)
    texts = ["A+", "B+", "C+", "A-", "B-", "C-"] * numMagnets
    return texts, currentPositions

def main():
    controlManager = pw.ControlManager()

    labels = ["Hello", "There", "General", "Kenobi"]
    controlManager["textBoxes"] = pw.TextBoxes((0.5, 0.0), (0.5, 1.0), labels = labels)

    x, y = controlManager.getSize()
    w, h = 500, 500
    controlManager["freeDraw"] = pw.FreeDraw((0, 0), (w / x, h / y))

    middleVec = pg.math.Vector2(0.5, 0.5)
    numMagnets = 2
    texts, currentPositions = getTextAndPos(numMagnets)
    def renderCurrentVector(ix):
        pos = currentPositions[ix]
        arrowDelta = pg.math.Vector2(pos[0], pos[1]) - middleVec
        controlManager["freeDraw"].arrow(middleVec, middleVec + arrowDelta, 3, (255, 255, 255))

    t0 = perf_counter()
    controlManager.update()
    while controlManager.isRunning():

        controlManager["freeDraw"].fill()

        t = perf_counter() - t0
        controlManager["textBoxes"].setTexts([str(t), f"{t:.2f}", f"{t:.0f}"])

        renderCurrentVector(round(t) % (6 * numMagnets))
        # controlManager["freeDraw"].arrow(middleVec, middleVec + arrowDelta, 3, (255, 255, 255))

        for (text, pos) in zip(texts, currentPositions):
            pos -= middleVec
            pos *= 1.1
            pos += middleVec
            controlManager["freeDraw"].text(pos, text, 18, (255, 255, 255))

        controlManager["freeDraw"].circle(middleVec, 0.4, (255, 255, 255))


        controlManager.update()

if __name__ == "__main__":
    main()
