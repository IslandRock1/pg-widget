
class Lowpass:
    def __init__(self, a):
        self.__a = a
        self.__prevOut = None

    def update(self, value):
        if (self.__prevOut is None):
            self.__prevOut = value

        self.__prevOut = self.__a * self.__prevOut + (1 - self.__a) * value
        return self.__prevOut

    def getValue(self):
        return self.__prevOut