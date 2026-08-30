from enum import Enum


# enums
# "E" for "enum" + first letter of unit type


class Metric:
    class Scale(Enum):
        mili = -3
        centi = -2
        deci = -1
        base = 0
        kilo = 3

    class EDist(Enum):
        mm = 0
        cm = 1
        dm = 2
        m = 3
        km = 4

    class ETemp(Enum):
        c = 0
        k = 1

    class EWeight(Enum):
        mg = 0
        cg = 1
        dg = 2
        g = 3
        kg = 4

    class Distance:
        def __init__(self, value: float, unit: str) -> None:
