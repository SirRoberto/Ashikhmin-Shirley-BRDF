import numpy as np
from math import atan, acos, degrees, radians, sin, cos

class PointLight():
    def __init__(self, pos:np.array, power):
        self.pos = pos
        self.power = power

        self.r = np.linalg.norm(pos)
        self.a = degrees(acos(pos[1] / self.r))
        if abs(pos[0]) > 1e-10:
            self.b = degrees(atan(pos[0] / pos[2]))
        else:
            self.b = 0


    def left(self, alpha=1):
        self.b -= alpha
        self.__cals_pos()


    def right(self, alpha=1):
        self.b += alpha
        self.__cals_pos()


    def up(self, alpha=1):
        self.a -= alpha
        self.__cals_pos()


    def down(self, alpha=1):
        self.a += alpha
        self.__cals_pos()


    def out_(self, alpha):
        self.r += alpha
        self.__cals_pos()


    def in_(self, alpha):
        self.r -= alpha
        self.__cals_pos()


    def __cals_pos(self):
        a = radians(self.a)
        b = radians(self.b)

        z = self.r * sin(a) * cos(b)
        x = self.r * sin(a) * sin(b)
        y = self.r * cos(a)

        self.pos = np.array([x,y,z])
