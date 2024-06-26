from __future__ import annotations
from typing import TYPE_CHECKING


class CombinedUnit:
    def __init__(
        self,
        numerator: list[Unit] = [],
        denominator: list[Unit] = [],
        total_factor: float = 1,
    ):
        self.__numerator = []
        self.__denominator = []
        self.__total_factor = total_factor

        for unit in numerator:
            factor, unit = self.__getFactorAndUnit(self.__numerator, unit)
            self.__total_factor *= factor
            self.__numerator.append(unit)
        for unit in denominator:
            factor, unit = self.__getFactorAndUnit(self.__denominator, unit)
            self.__total_factor /= factor
            self.__denominator.append(unit)

    def __str__(self) -> str:
        def formatUnitList(unit_list: list[Unit]) -> str:
            unit_list = [str(unit) for unit in unit_list]
            new_unit_list = []
            unit_set = set(unit_list)
            for unit in unit_set:
                if unit_list.count(unit) > 1:
                    new_unit_list.append(f"{unit}^{unit_list.count(unit)}")
                else:
                    new_unit_list.append(unit)
            unit_text = " * ".join(new_unit_list)
            if unit_text == "":
                unit_text = "1"
            return unit_text

        return f"{formatUnitList(self.numerator)}{"/" + formatUnitList(self.denominator) if self.denominator else ''}"

    def __repr__(self) -> str:
        return f"{self.numerator}/{self.denominator}"

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, CombinedUnit):
            return False
        return str(self) == str(value)

    @property
    def numerator(self) -> list[Unit]:
        return self.__numerator

    @property
    def denominator(self) -> list[Unit]:
        return self.__denominator

    @property
    def total_factor(self) -> float:
        return self.__total_factor

    @total_factor.setter
    def settotal_factor(self, value: float) -> CombinedUnit:
        total_factor = value
        return self.__class__(self.numerator, self.denominator, total_factor)

    @staticmethod
    def __getFactorAndUnit(
        existing_units: list[Unit], new_unit: Unit
    ) -> tuple[float, Unit]:
        for existing_unit in existing_units:
            if existing_unit.__class__ == new_unit.__class__:
                return new_unit.convert(new_unit, existing_unit)
        return 1, new_unit

    def __adjustUnits(
        self, unit: Unit, type: str
    ) -> tuple[float, list[Unit], list[Unit]]:

        type_dict = {
            "numerator": (self.__numerator.copy(), self.__denominator.copy()),
            "denominator": (self.__denominator.copy(), self.__numerator.copy()),
        }
        type1, type2 = type_dict[type]
        factor1, unit = self.__getFactorAndUnit(type1, unit)
        factor2, unit = self.__getFactorAndUnit(type2, unit)
        factor = factor1 / factor2
        if unit in type2:
            type2.remove(unit)
            return factor, type1, type2
        type1.append(unit)
        return factor, type1, type2

    def addNumerator(self, unit: Unit) -> CombinedUnit:
        factor, numerator, denominator = self.__adjustUnits(unit, "numerator")
        return CombinedUnit(numerator, denominator, factor * self.total_factor)

    def addDenominator(self, unit: Unit) -> CombinedUnit:
        factor, denominator, numerator = self.__adjustUnits(unit, "denominator")
        return CombinedUnit(numerator, denominator, self.total_factor / factor)

    def __truediv__(self, other: Unit | CombinedUnit) -> CombinedUnit:
        if isinstance(other, Unit):
            return self.addDenominator(other)
        elif isinstance(other, CombinedUnit):
            for unit in other.numerator:
                self = self.addDenominator(unit)
            for unit in other.denominator:
                self = self.addNumerator(unit)

            return self

    def __mul__(self, other: Unit | CombinedUnit) -> CombinedUnit:
        if isinstance(other, Unit):
            return self.addNumerator(other)
        elif isinstance(other, CombinedUnit):
            for unit in other.numerator:
                self = self.addNumerator(unit)
            for unit in other.denominator:
                self = self.addDenominator(unit)
            return self

    def convertUnit(self, to_unit: Unit) -> CombinedUnit:
        def adjustUnits(units: list[Unit]) -> list[Unit]:
            new_units = []
            adjust_factor = 1
            for unit in units:
                try:
                    new_factor, new_unit = unit.convert(unit, to_unit)
                    adjust_factor *= new_factor
                    new_units.append(new_unit)
                except TypeError:
                    new_units.append(unit)
            return new_units, adjust_factor

        new_numerator, adjust_factor_numerator = adjustUnits(self.numerator)
        new_denominator, adjust_factor_denominator = adjustUnits(self.denominator)

        return self.__class__(
            new_numerator,
            new_denominator,
            self.total_factor * adjust_factor_numerator / adjust_factor_denominator,
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
        cls, from_unit: Unit | None, to_unit: Unit
    ) -> tuple[float, Unit]:
        if from_unit is None:
            return 1, to_unit
        if from_unit.__class__ != to_unit.__class__:
            raise TypeError("Units must be of the same type")
        return from_unit.FACTOR_DICT[from_unit] / from_unit.FACTOR_DICT[to_unit], to_unit

    def __truediv__(self, other: Unit | "CombinedUnit") -> "CombinedUnit":
        if isinstance(other, CombinedUnit):
            return CombinedUnit([self]) / other
        return CombinedUnit([self]).addDenominator(other)

    def __mul__(self, other: Unit | "CombinedUnit") -> "CombinedUnit":
        if isinstance(other, CombinedUnit):
            return CombinedUnit([self]) * other
        return CombinedUnit([self]).addNumerator(other)
