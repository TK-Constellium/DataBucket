from __future__ import annotations


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
            str_unit_list = [str(unit) for unit in unit_list]
            new_unit_list = []
            unit_set = set(str_unit_list)
            for unit in unit_set:
                if str_unit_list.count(unit) > 1:
                    new_unit_list.append(f"{unit}^{str_unit_list.count(unit)}")
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

    @property
    def is_none(self) -> bool:
        return not self.numerator and not self.denominator

    def resetTotalFactor(self) -> CombinedUnit:
        return self.__class__(self.numerator, self.denominator, 1)

    @staticmethod
    def __getFactorAndUnit(
        existing_units: list[Unit], new_unit: Unit
    ) -> tuple[float, Unit]:
        for existing_unit in existing_units:
            if existing_unit.__class__ == new_unit.__class__:
                return new_unit.convert(existing_unit)
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

    def __addNumerator(self, unit: Unit) -> CombinedUnit:
        factor, numerator, denominator = self.__adjustUnits(unit, "numerator")
        return CombinedUnit(numerator, denominator, factor * self.total_factor)

    def __addDenominator(self, unit: Unit) -> CombinedUnit:
        factor, denominator, numerator = self.__adjustUnits(unit, "denominator")
        return CombinedUnit(numerator, denominator, self.total_factor / factor)

    def __truediv__(self, other: Unit | CombinedUnit) -> CombinedUnit:
        if isinstance(other, Unit):
            return self.__addDenominator(other)
        elif isinstance(other, CombinedUnit):
            for unit in other.numerator:
                self = self.__addDenominator(unit)
            for unit in other.denominator:
                self = self.__addNumerator(unit)

            return self

    def __mul__(self, other: Unit | CombinedUnit) -> CombinedUnit:
        if isinstance(other, Unit):
            return self.__addNumerator(other)
        elif isinstance(other, CombinedUnit):
            for unit in other.numerator:
                self = self.__addNumerator(unit)
            for unit in other.denominator:
                self = self.__addDenominator(unit)
            return self

    def __rtruediv__(self, other: Unit) -> CombinedUnit:
        return CombinedUnit([other]) / self
    
    def __rmul__(self, other: Unit) -> CombinedUnit:
        return self.__addNumerator(other)
    
    def __floordiv__(self, other: Unit | CombinedUnit) -> CombinedUnit:
        return self.__truediv__(other)
    
    def __mod__(self, other: Unit | CombinedUnit) -> CombinedUnit:
        return self.__truediv__(other)

    def convert(self, to_unit: Unit | CombinedUnit) -> CombinedUnit:
        def adjustUnits(units: list[Unit], to_unit: Unit) -> tuple[list[Unit], float]:
            new_units = []
            adjust_factor = 1
            for unit in units:
                try:
                    new_factor, new_unit = unit.convert(to_unit)
                    adjust_factor *= new_factor
                    new_units.append(new_unit)
                except TypeError:
                    new_units.append(unit)
            return new_units, adjust_factor
        
        new_numerator = self.numerator
        new_denominator = self.denominator
        unit_list = [to_unit] if isinstance(to_unit, Unit) else to_unit.numerator + to_unit.denominator
        total_factor = self.total_factor
        for unit in unit_list:
            new_numerator, adjust_factor_numerator = adjustUnits(new_numerator, unit)
            new_denominator, adjust_factor_denominator = adjustUnits(new_denominator, unit)
            total_factor *= adjust_factor_numerator / adjust_factor_denominator

        return self.__class__(
            new_numerator,
            new_denominator,
            total_factor,
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
        if not isinstance(value, Unit): # Maybe a bug here i.e. Length will be equal to Weight, because they are both instances of Unit
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

    @property
    def is_none(self) -> bool:
        return False
    
    def convert(
        self, to_unit: Unit
    ) -> tuple[float, Unit]:
        if self.__class__ != to_unit.__class__:
            raise TypeError("Units must be of the same type")
        return self.FACTOR_DICT[self] / self.FACTOR_DICT[to_unit], to_unit

    def __truediv__(self, other: Unit | CombinedUnit) -> CombinedUnit:
        return CombinedUnit([self]) / other
    
    def __mul__(self, other: Unit | CombinedUnit) -> CombinedUnit:
        return CombinedUnit([self]) * other
