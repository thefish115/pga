from pga import Blades
from tkinter import Canvas
from timeit import default_timer as t


class Bounds:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
    
    def boundary(self):
        return [
            (self.xmax * Blades.e20 + self.ymax * Blades.e01 + 1*Blades.e12)
            | (self.xmax * Blades.e20 + self.ymin * Blades.e01 + 1*Blades.e12),

            (self.xmin * Blades.e20 + self.ymax * Blades.e01 + 1*Blades.e12)
            | (self.xmin * Blades.e20 + self.ymin * Blades.e01 + 1*Blades.e12),

            (self.xmin * Blades.e20 + self.ymax * Blades.e01 + 1*Blades.e12)
            | (self.xmax * Blades.e20 + self.ymax * Blades.e01 + 1*Blades.e12),

            (self.xmin * Blades.e20 + self.ymin * Blades.e01 + 1*Blades.e12)
            | (self.xmax * Blades.e20 + self.ymin * Blades.e01 + 1*Blades.e12),
        ]


class GACanvas(Canvas):
    def __init__(self, master, bounds: Bounds, obs, dt) -> None:
        super().__init__(master)
        self.bounds = bounds
        self.obs = obs
        self.dt = dt
        self.t0 = t()

    def c2p(self, xc, yc):
        strGeo = str(self.master.master.geometry())
        w = int(strGeo[:strGeo.find('x')])
        h = int(strGeo[strGeo.find('x')+1:strGeo.find('+')])
        xp = int(w * (xc - self.bounds.xmin) /
                 (self.bounds.xmax - self.bounds.xmin))
        yp = int(h * (yc - self.bounds.ymax) /
                 (self.bounds.ymin - self.bounds.ymax))
        return (xp, yp)

    def drawObjects(self, t):
        for ob in self.obs:
            ob.draw(self, t)

    def gett(self):
        return t() - self.t0

    def animate(self):
        self.update()
        self.drawObjects(self.gett())
        self.master.master.after(self.dt, self.animate)
