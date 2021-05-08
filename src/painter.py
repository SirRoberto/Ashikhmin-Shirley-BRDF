from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget

from reflection import AshikhminShirleyModel
from shapes import Sphere
from lights import PointLight
import numpy as np

import threading, time

class Painter(QPainter):
    def __init__(self, widget:QWidget):
        super().__init__(widget)
        self.widget = widget
        self.scale_ = 1.
        self.scale(self.scale_, self.scale_)


    def paintSphere(self, sphere:Sphere, light:PointLight):
        num_intervals = 1
        points = [-sphere.r]
        for i in range(num_intervals):
            points.append(points[-1]+round((2*sphere.r+1)/num_intervals))

        intervals = []
        tmp = points[0]
        for p in points[1:]:
            intervals.append([tmp, p])
            tmp = p
            
        try:
            threads = []
            for i in intervals:
                for j in intervals:
                    t = threading.Thread( target=self.paintPartOfSphere, args=(sphere, light, i, j,) )
                    threads.append(t)
                    t.start()

            for t in threads:
                t.join()
        except:
            print("Error: unable to start thread")



    def paintPartOfSphere(self, sphere:Sphere, light:PointLight, f, t):
        m = AshikhminShirleyModel()

        cX = self.widget.width()/self.scale_/2
        cY = self.widget.height()/self.scale_/2

        for i, x in enumerate(range(f[0], f[1])):
            for j, y in enumerate(range(t[0], t[1])):
                z = sphere.getZ(x, y)
                if z > 0:
                    I = m.render_pixel(light, np.array([x,y,z]), np.array([0,0,1]))
                    self.setPen(QColor.fromRgbF(I[0], I[1], I[2]))
                    self.drawPoint(x+cX, -y+cY)