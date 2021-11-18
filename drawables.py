from abc import ABC, abstractmethod
from pga import _Multivector, Blades, rotor, motor
from math import pi


class Drawable(ABC):
    @abstractmethod
    def draw(self, canvas):
        pass

    @abstractmethod
    def mote(self, t):
        pass


class Point(Drawable):
    def __init__(self, m: _Multivector, motor, color) -> None:
        self.mv = m
        self.motor = motor
        self.img = None
        self.color = color

    def draw(self, canvas, t):
        c2p = canvas.c2p
        canvas.delete(self.img)
        pt = self.mote(t)
        xp, yp = c2p(pt[Blades.e20], pt[Blades.e01])
        self.img = canvas.create_oval(xp-3, yp-3, xp+3, yp+3, fill=self.color)

    def mote(self, t):
        return self.mv.mote(self.motor(t))


class LineSegment(Drawable):
    def __init__(self, p0: _Multivector, p1: _Multivector, motor, color) -> None:
        self.motor = motor
        self.color = color
        self.p0 = p0
        self.p1 = p1
        self.img = None

    def draw(self, canvas, t):
        c2p = canvas.c2p
        canvas.delete(self.img)
        p0t, p1t = self.mote(t)
        xp0, yp0 = c2p(p0t[Blades.e20], p0t[Blades.e01])
        xp1, yp1 = c2p(p1t[Blades.e20], p1t[Blades.e01])
        self.img = canvas.create_line(xp0, yp0, xp1, yp1, fill=self.color)

    def mote(self, t):
        m = lambda p: p.mote(self.motor(t))
        return (
            m(self.p0),
            m(self.p1),
        )

class Axes(Drawable):
    def __init__(self, xColor, yColor) -> None:
        super().__init__()
        self.xColor = xColor
        self.yColor = yColor
        self.xImg = None
        self.yImg = None

    def draw(self, canvas, t):
        def drawLine(xc0, yc0, xc1, yc1, color):
            xp0, yp0 = canvas.c2p(xc0, yc0)
            xp1, yp1 = canvas.c2p(xc1, yc1)
            return canvas.create_line(xp0, yp0, xp1, yp1, fill=color)
        canvas.delete(self.xImg)
        canvas.delete(self.yImg)
        self.yImg = drawLine(0, canvas.bounds.ymax, 0, canvas.bounds.ymin, self.yColor)
        self.xImg = drawLine(canvas.bounds.xmax, 0, canvas.bounds.xmin, 0, self.xColor)
    def mote(self, t):
        return self

class Polygon(Drawable):
    def __init__(self, verticies: list[_Multivector], motorFuncs, color) -> None:
        if len(motorFuncs) == 3:
            self.motor = lambda t: rotor(motorFuncs[0](
                t), motorFuncs[1](t), motorFuncs[2](t))
        elif len(motorFuncs) == 2:
            self.motor = lambda t: motor(motorFuncs[0](t), motorFuncs[1](t))
        self.color = color
        self.verticies = [Point(v, self.motor, self.color) for v in verticies]
        self.edges = [LineSegment(self.verticies[i].mv, self.verticies[i+1 if i+1 < len(
            self.verticies) else 0].mv, self.motor, self.color) for i in range(len(verticies))]

    def getCenter(self):
        mv = 0*Blades.SCALAR
        for p in self.verticies:
            mv = mv + p.mv
        return mv[Blades.e20] / mv[Blades.e12] * Blades.e20 + mv[Blades.e01] / mv[Blades.e12] * Blades.e01 + 1*Blades.e12

    def draw(self, canvas, t):
        for v in self.verticies:
            v.draw(canvas, t)
        for e in self.edges:
            e.draw(canvas, t)

    def mote(self, t):
        for v in self.verticies:
            v.mote(t)
        for e in self.edges:
            e.mote(t)

class CenterBoundPolygon(Drawable):
    def __init__(self, verticies: list[_Multivector], motorFuncs, color) -> None:
        self.color = color
        self.center = CenterBoundPolygon.getCenter(verticies)
        self.verticies = [v + -1.0*Blades.SCALAR*self.center for v in verticies]
        self.motor = lambda t: motor(motorFuncs[1](t), motorFuncs[2](t))
        self.thetaFunc = motorFuncs[0]
        self.imgs = []

    def getCenter(verticies):
        mv = 0*Blades.SCALAR
        for v in verticies:
            mv = mv + v
        return mv[Blades.e20] / mv[Blades.e12] * Blades.e20 + mv[Blades.e01] / mv[Blades.e12] * Blades.e01 + 1*Blades.e12

    def getRotor(self, t):
        return rotor(self.thetaFunc(t), self.center[Blades.e20], self.center[Blades.e01])

    def draw(self, canvas, t):

        c2p = canvas.c2p
        points,edges = self.mote(t)
        for i in self.imgs:
            canvas.delete(i)
        for p in points:
            xp, yp = c2p(p[Blades.e20], p[Blades.e01])
            self.imgs.append(canvas.create_oval(xp-3, yp-3, xp+3, yp+3, fill=self.color))
        for e in edges:
            xp0, yp0 = c2p(e[0][Blades.e20], e[0][Blades.e01])
            xp1, yp1 = c2p(e[1][Blades.e20], e[1][Blades.e01])
            self.imgs.append(canvas.create_line(xp0, yp0, xp1, yp1, fill=self.color))

    def mote(self, t):
        centerT = self.center.mote(self.motor(t))
        verticiesT = [v.mote(self.getRotor(t)) for v in self.verticies]
        points = [centerT + v for v in verticiesT]
        edges = [(points[i], points[i+1 if i+1 < len(points) else 0]) for i in range(len(points))]
        return points, edges

class RegularPolygon(Polygon):
    def __init__(self, center: _Multivector, radius, vertexNumber, motorFuncs, color) -> None:
        verticies = []
        for i in range(vertexNumber):
            verticies.append(
                (center + radius*Blades.e20).mote(
                    rotor(2.0*pi/vertexNumber*i, center[Blades.e20], center[Blades.e01])))
        super().__init__(verticies, motorFuncs, color)

class EquilateralTriangle(RegularPolygon):
    def __init__(self, center: _Multivector, radius, motorFuncs, color) -> None:
        super().__init__(center, radius, 3, motorFuncs, color)

class Square(RegularPolygon):
    def __init__(self, center: _Multivector, radius, motorFuncs, color) -> None:
        super().__init__(center, radius, 4, motorFuncs, color)
