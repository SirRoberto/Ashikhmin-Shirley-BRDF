from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsBlurEffect
from shapes import Sphere
from controler import Controler
from painter import Painter
from lights import PointLight
from numpy import array


SIZE_X = 450
SIZE_Y = 450

class Scene(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.interface()
        self.createObject()
        self.pointLight = PointLight(array([-5000,5000,10000]), 100)
        self.controler = Controler(self.pointLight)
        self.keylist = []


    def interface(self):
        self.resize(SIZE_X, SIZE_Y)
        self.setWindowTitle("Wirtualna kamera")
        self.setStyleSheet("background-color: black;")


    def createObject(self):
        self.sphere = Sphere()


    def paintEvent(self, event):
        render = Painter(self)
        render.paintSphere(self.sphere, self.pointLight)


    def keyPressEvent(self, event):
        self.firstrelease = True
        self.keylist.append(event.key())


    def keyReleaseEvent(self, event):
        if self.firstrelease == True: 
            self.processmultikeys(self.keylist)
        self.firstrelease = False
        del self.keylist[-1]


    def processmultikeys(self,keyspressed):
        for key in keyspressed:
            try:
                self.controler.panel[key]()
            except:
                pass
        self.update()