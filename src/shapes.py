from math import sqrt
import numpy as np

class Sphere():

    def __init__(self, radius=200):
        self.r = radius


    def getZ(self, x, y):
        if self.r*self.r - x*x - y*y < 0:
            return -1
        return sqrt(self.r*self.r - x*x - y*y)

