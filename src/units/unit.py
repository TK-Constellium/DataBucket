from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataBucket.src.auxiliary.value import NumberValue


class CombinedUnit:
    def __init__(
        self, numerator: "Unit" | "CombinedUnit", denominator: "Unit" | "CombinedUnit"
    ):
        self.__numerator = numerator
        self.__denominator = denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

    def __repr__(self):
        return f"{self.numerator}/{self.denominator}"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, CombinedUnit):
            return False
        return str(self) == str(value)

    @property
    def numerator(self):
        return self.__numerator

    @property
    def denominator(self):
        return self.__denominator

    def __truediv__(self, other: "Unit" | "CombinedUnit") -> "CombinedUnit":
        if isinstance(other, Unit):
            return CombinedUnit(self, other)
        raise TypeError("Division is only supported between Unit instances")

    def convertNumerator(
        self, value: NumberValue | float, to_unit: "Unit"
    ) -> NumberValue | float:
        return (
            Unit.convert(value, self.numerator, to_unit),
            self.__class__(to_unit, self.denominator),
        )

    def convertDenominator(
        self, value: NumberValue | float, to_unit: "Unit"
    ) -> NumberValue | float:
        return (
            1 / Unit.convert(value, self.numerator, to_unit),
            self.__class__(to_unit, self.denominator),
        )


class Unit:
    FACTOR_DICT: dict[Unit, float]

    def __init__(self, name: str, symbol: str):
        self.__name = name
        self.__symbol = symbol

    def __str__(self):
        return f"{self.symbol}"

    def __repr__(self):
        return f"{self.name.upper()}"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Unit):
            return False
        return self.name == value.name

    def __hash__(self):
        return hash(self.name)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def symbol(self) -> str:
        return self.__symbol

    @classmethod
    def convert(
        cls, value: NumberValue | float, from_unit: "Unit" | None, to_unit: "Unit"
    ) -> NumberValue | float:
        if from_unit.__class__ != to_unit.__class__:
            raise TypeError("Units must be of the same type")
        new_value = (
            value * from_unit.FACTOR_DICT[from_unit] / from_unit.FACTOR_DICT[to_unit]
        )
        return new_value, to_unit

    def __truediv__(self, other: "Unit" | "CombinedUnit") -> "CombinedUnit":
        if isinstance(other, Unit):
            return CombinedUnit(self, other)
        raise TypeError("Division is only supported between Unit instances")
