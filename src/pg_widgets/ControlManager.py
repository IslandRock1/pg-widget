
import time
import os

import numpy as np
import pygame as pg

from .basics.UIGroup import UIGroup
from .utils.Lowpass import Lowpass

class ControlManager:
    def __init__(self):

        self.__size = (1200, 600)
        self.__screen = pg.display.set_mode(self.__size, pg.RESIZABLE)
        self.__uiGroup = UIGroup((0, 0), (1.0, 1.0))
        self.__uiGroup.changeSize(self.__size)

        self.__bgColor = (50, 50, 50)
        self.__running = True
        self.__isRecording = False
        self.__writerExist = False
        self.__iter = 0

        self.__fpsLowpass = Lowpass(0.9)

    def close(self):

        if (self.__writerExist):
            self.__writer.close()

    def __getitem__(self, item):
        return self.__uiGroup[item]

    def __setitem__(self, key, value):
        self.__uiGroup[key] = value
        self.__uiGroup[key].changeSize(self.__size)

    def isRunning(self):
        return self.__running

    def getSize(self):
        return self.__size

    def getIteration(self):
        return self.__iter

    def getRenderTime(self):
        v = self.__fpsLowpass.getValue()
        if (v is None): return -1
        return v

    def screenshot(self):
        os.makedirs("screenshots", exist_ok=True)
        pg.image.save(self.__screen, f"screenshots/frame_{self.__iter}.png")

    def startRecording(self):
        self.__isRecording = True
        os.makedirs("frames", exist_ok=True)
        os.makedirs("video", exist_ok=True)

        import imageio
        self.__writerExist = True
        self.__writer = imageio.get_writer(f"video/{time.perf_counter()}.mp4", fps=60)

    def stopRecording(self):
        self.__isRecording = False

    def __handleKeyboard(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.__running = False

                elif event.key == pg.K_r:
                    self.startRecording()

                elif event.key == pg.K_f:
                    self.stopRecording()

                elif event.key == pg.K_s:
                    self.screenshot()

        w, h = pg.display.get_window_size()
        if (w != self.__size[0]) or (h != self.__size[1]):
            self.__size = (w, h)

            self.__uiGroup.changeSize((w, h))

    def __handleMouse(self):
        pressed = pg.mouse.get_pressed()
        pos = pg.mouse.get_pos()

        self.__uiGroup.update(pressed, pos)

    def __informationControl(self):
        pass

    def __render(self):
        self.__screen.fill(self.__bgColor)
        self.__screen.blit(self.__uiGroup.render(self.__bgColor), self.__uiGroup.getPos())
        pg.display.flip()

        if (self.__isRecording):
            frame = pg.surfarray.array3d(self.__screen)
            frame = np.transpose(frame, (1, 0, 2))
            self.__writer.append_data(frame)

    def update(self):
        t0 = time.perf_counter()
        if not self.__running:
            return
        self.__iter += 1

        self.__handleKeyboard()
        self.__handleMouse()
        self.__informationControl()
        self.__render()
        t1 = time.perf_counter()
        self.__fpsLowpass.update(t1 - t0)