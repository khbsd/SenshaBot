import re
from enum import Enum


# enums
# "E" for "enum" + first letter of unit type
class EScale(Enum):
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


class Measurement:
    def __init__(self, value: float, unit: str) -> None:
        self.value: float = value
        self.unit: str = unit
        self.scale: EScale = self.get_scale()
        self.target: EDist | ETemp | EWeight = self.get_target()

    def get_scale(self) -> EScale:
        if len(self.unit) > 1:
            s = self.unit[0]
            for scale in EScale:
                if scale.name[0] == s:
                    return scale

        return EScale.base

    def get_target(self) -> EDist | ETemp | EWeight:
        target_list = [EDist, ETemp, EWeight]

        for e in target_list:
            for name in e:
                if self.unit[-1].lower() == name.name:
                    return name
        return EDist.m


class Metric:
    def __init__(self):
        self.re: re.Pattern = re.compile(
            r"(?P<amount>[\d]+[.,]*[\d]*)[\s]*(?P<unit>[acdEfhkMmnPpRrTQqYyZzμ]*[mkcgf]+)"
        )

    def parser(self, text: str) -> Measurement | None:
        m = self.re.match(text.lower())
        if m:
            value = m.group("amount").replace(",", ".")
            value = float(value)
            unit = m.group("unit")
            return Measurement(value, unit)
        return None


t_list = [
    "45g",
    "23.5 cm",
    "768,43kM",
    "67,765 mg",
    "54c",
    "23k"
]

for t in t_list:
    m = Metric().parser(t)
    if m is not None:
        print(t, m.scale, m.target, m.unit, m.value)
