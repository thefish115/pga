from __future__ import annotations
from enum import Enum
from numbers import Number
from itertools import product
import math

_multab = {}


class Blades(Enum):
    SCALAR = '1'
    e0 = 'e\u2080'
    e1 = 'e\u2081'
    e2 = 'e\u2082'
    e20 = 'e\u2082\u2080'
    e01 = 'e\u2080\u2081'
    e12 = 'e\u2081\u2082'
    I = 'I'

    def __mul__(self, other):
        if type(other) == type(Blades.SCALAR):
            return _multab[self][other]
        elif isinstance(other, Number):
            out = _Multivector(None)
            out[self] = other
            return out

    def __rmul__(self, other):
        if isinstance(other, Number):
            return self * other


_multab = {
    Blades.SCALAR: {
        Blades.SCALAR: (Blades.SCALAR,    1),
        Blades.e0:     (Blades.e0,        1),
        Blades.e1:     (Blades.e1,        1),
        Blades.e2:     (Blades.e2,        1),
        Blades.e20:    (Blades.e20,       1),
        Blades.e01:    (Blades.e01,       1),
        Blades.e12:    (Blades.e12,       1),
        Blades.I:      (Blades.I,         1),
    },
    Blades.e0: {
        Blades.SCALAR: (Blades.e0,        1),
        Blades.e0:     (Blades.SCALAR,    0),
        Blades.e1:     (Blades.e01,       1),
        Blades.e2:     (Blades.e20,       -1),
        Blades.e20:    (Blades.SCALAR,    0),
        Blades.e01:    (Blades.SCALAR,    0),
        Blades.e12:    (Blades.I,         1),
        Blades.I:      (Blades.SCALAR,    0),
    },
    Blades.e1: {
        Blades.SCALAR: (Blades.e1,        1),
        Blades.e0:     (Blades.e01,       -1),
        Blades.e1:     (Blades.SCALAR,    1),
        Blades.e2:     (Blades.e12,       1),
        Blades.e20:    (Blades.I,         1),
        Blades.e01:    (Blades.e0,        -1),
        Blades.e12:    (Blades.e2,        1),
        Blades.I:      (Blades.e20,       1),
    },
    Blades.e2: {
        Blades.SCALAR: (Blades.e2,        1),
        Blades.e0:     (Blades.e20,       1),
        Blades.e1:     (Blades.e12,       -1),
        Blades.e2:     (Blades.SCALAR,    1),
        Blades.e20:    (Blades.e0,        1),
        Blades.e01:    (Blades.I,         1),
        Blades.e12:    (Blades.e1,        -1),
        Blades.I:      (Blades.e01,       1),
    },
    Blades.e20: {
        Blades.SCALAR: (Blades.e20,       1),
        Blades.e0:     (Blades.SCALAR,    0),
        Blades.e1:     (Blades.I,         1),
        Blades.e2:     (Blades.e0,        -1),
        Blades.e20:    (Blades.SCALAR,    0),
        Blades.e01:    (Blades.SCALAR,    0),
        Blades.e12:    (Blades.e01,       1),
        Blades.I:      (Blades.SCALAR,    0),
    },
    Blades.e01: {
        Blades.SCALAR: (Blades.e01,       1),
        Blades.e0:     (Blades.SCALAR,    0),
        Blades.e1:     (Blades.e0,        1),
        Blades.e2:     (Blades.I,         1),
        Blades.e20:    (Blades.SCALAR,    0),
        Blades.e01:    (Blades.SCALAR,    0),
        Blades.e12:    (Blades.e20,       -1),
        Blades.I:      (Blades.SCALAR,    0),
    },
    Blades.e12: {
        Blades.SCALAR: (Blades.e12,       1),
        Blades.e0:     (Blades.I,         1),
        Blades.e1:     (Blades.e2,        -1),
        Blades.e2:     (Blades.e1,        1),
        Blades.e20:    (Blades.e01,       -1),
        Blades.e01:    (Blades.e20,       1),
        Blades.e12:    (Blades.SCALAR,    -1),
        Blades.I:      (Blades.e0,        -1),
    },
    Blades.I: {
        Blades.SCALAR: (Blades.I,         1),
        Blades.e0:     (Blades.SCALAR,    0),
        Blades.e1:     (Blades.e20,       1),
        Blades.e2:     (Blades.e01,       1),
        Blades.e20:    (Blades.SCALAR,    0),
        Blades.e01:    (Blades.SCALAR,    0),
        Blades.e12:    (Blades.e0,        -1),
        Blades.I:      (Blades.SCALAR,    0),
    },
}

e = None


class _Multivector(dict):
    def __init__(self, m: _Multivector) -> None:
        if m is None:
            for blade in Blades:
                self[blade] = 0
            return
        for k, v in m.items():
            self[k] = v

    def __add__(self, other: _Multivector) -> _Multivector:
        out = _Multivector(None)
        for (k, vs), (_, vo) in zip(self.items(), other.items()):
            out[k] = vs + vo
        return out

    def __mul__(self, other) -> _Multivector:
        if isinstance(other, Number):
            return self * (other * Blades.SCALAR)
        out = _Multivector(None)
        rawPoduct = [(ks * ko, vs * vo) for (ks, vs), (ko, vo)
                     in product(self.items(), other.items())]
        for c, v in rawPoduct:
            out = out + v*c[1]*c[0]
        return out

    def grade(self):
        if self[Blades.I] != 0:
            return 3
        elif any([self[blade] != 0 for blade in [Blades.e20, Blades.e01, Blades.e12]]):
            return 2
        elif any([self[blade] != 0 for blade in [Blades.e0, Blades.e1, Blades.e2]]):
            return 1
        else:
            return 0

    def gradeSelect(self, grade):
        if grade == 0:
            return self[Blades.SCALAR]*Blades.SCALAR
        elif grade == 1:
            return self[Blades.e0]*Blades.e0 + self[Blades.e1]*Blades.e1 + self[Blades.e2]*Blades.e2
        elif grade == 2:
            return self[Blades.e20]*Blades.e20 + self[Blades.e01]*Blades.e01 + self[Blades.e12]*Blades.e12
        elif grade == 3:
            return self[Blades.I]*Blades.I

    def __xor__(self, other):
        return (self*other).gradeSelect(self.grade() + other.grade())

    def dual(self):
        return (
            self[Blades.I]*Blades.SCALAR
            + self[Blades.e12]*Blades.e0
            + self[Blades.e20]*Blades.e1
            + self[Blades.e01]*Blades.e2
            + self[Blades.e1]*Blades.e20
            + self[Blades.e2]*Blades.e01
            + self[Blades.e0]*Blades.e12
            + self[Blades.SCALAR]*Blades.I
        )

    def reverseMV(self):
        return (
            self[Blades.SCALAR]*Blades.SCALAR
            + self[Blades.e0]*Blades.e0
            + self[Blades.e1]*Blades.e1
            + self[Blades.e2]*Blades.e2
            + -1*self[Blades.e20]*Blades.e20
            + -1*self[Blades.e01]*Blades.e01
            + -1*self[Blades.e12]*Blades.e12
            + -1*self[Blades.I]*Blades.I
        )

    def __or__(self, other):
        return (self.dual() ^ other.dual()).dual()

    def trueShape(self) -> dict[Blades, bool]:
        return {k: v != 0 for k, v in self.items()}

    def roughShape(self) -> list[bool]:
        ts = self.trueShape()
        return [
            ts[Blades.SCALAR] or ts[Blades.I],
            ts[Blades.e0] or ts[Blades.e1] or ts[Blades.e2],
            ts[Blades.e20] or ts[Blades.e01] or ts[Blades.e12],
        ]

    def isBivector(self) -> bool:
        rs = self.roughShape()
        return rs[2] and not rs[0] and not rs[1]
    
    def getEuclidean(self):
        if self.isBivector():
            return (1.0 / self[Blades.e12])*Blades.SCALAR*self

    def isVector(self) -> bool:
        rs = self.roughShape()
        return rs[1] and not rs[0] and not rs[2]

    def mote(self, motor) -> _Multivector:
        r = e**(motor)
        revR = r.reverseMV()
        return r*self*revR

    def __repr__(self) -> str:
        rep = ''
        for k, v in self.items():
            rep = rep + f'{k.value}\t{v}\n'
        return rep.strip()


class _E(_Multivector):
    def __init__(self) -> None:
        super().__init__(math.e*Blades.SCALAR)

    def __pow__(self, other):
        if all([v == 0.0 for v in other.values()]):
                return 1*Blades.SCALAR
        if other.isBivector():
            if other[Blades.e12] == 0:
                return 1*Blades.SCALAR + .5*other[Blades.e20]*Blades.e20 + .5*other[Blades.e01]*Blades.e01
            return math.cos(other[Blades.e12])*Blades.SCALAR + math.sin(other[Blades.e12]) / other[Blades.e12] * Blades.SCALAR * other
        return _Multivector(None)


e = _E()


def rotor(theta, x, y):
    return theta / 2.0 * Blades.SCALAR * (x * Blades.e20 + y * Blades.e01 + 1*Blades.e12)


r90_0_0 = rotor(math.pi/2.0, 0, 0)


def motor(dx, dy):
    return (dx*Blades.e20 + dy*Blades.e01).mote(r90_0_0)
