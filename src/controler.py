from lights import PointLight

class Controler():
    def __init__(self, light:PointLight):
        alpha = 5
        self.panel = {
            ord('W') : lambda : light.up(alpha),
            ord('S') : lambda : light.down(alpha),

            ord('A') : lambda : light.left(alpha),
            ord('D') : lambda : light.right(alpha),

            ord('Q') : lambda : light.in_(alpha/2),
            ord('E') : lambda : light.out_(alpha/2),
        }