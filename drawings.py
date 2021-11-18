from gaCanvas import Bounds
from pga import Blades
from drawables import Axes, CenterBoundPolygon, EquilateralTriangle, Polygon, Square
from math import cos, sin

def getBounds():
    return Bounds(-100, -100, 100, 100)


def getObs():
    verts = [
        80*Blades.e20 + 10*Blades.e01 + 1*Blades.e12,
        10*Blades.e20 + 80*Blades.e01 + 1*Blades.e12,
        10*Blades.e20 + 10*Blades.e01 + 1*Blades.e12,
    ]
    return [
        Axes('blue', 'red'),
        # Polygon(verts, (lambda t: t, lambda t: 3.0*t, lambda t: 3.0*t), 'green'),
        # Polygon(verts, (lambda t: 25.0*cos(t), lambda t: 25.0*sin(t)), 'orange'),
        # EquilateralTriangle(1*Blades.e12, 50, (lambda t: t, lambda _: 0.0, lambda _: 0.0), 'purple'),
        CenterBoundPolygon(verts,(lambda t: t,lambda t: 10.0*t,lambda t: 10.0*t,), 'green'),
    ]
# =================================================================================
def sampleBounds():
    return Bounds(-100, -100, 100, 100)


def sampleObs():
    verts = [
        80*Blades.e20 + 10*Blades.e01 + 1*Blades.e12,
        10*Blades.e20 + 80*Blades.e01 + 1*Blades.e12,
        10*Blades.e20 + 10*Blades.e01 + 1*Blades.e12,
    ]
    return [
        Axes('blue', 'red'),
        Polygon(verts, (lambda t: t, lambda t: 3.0*t, lambda t: 3.0*t), 'green'),
        Polygon(verts, (lambda t: 25.0*cos(t), lambda t: 25.0*sin(t)), 'orange'),
    ]