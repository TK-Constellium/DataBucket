from __future__ import annotations

from decimal import Decimal
from datetime import date, datetime, timedelta, timezone
from DataBucket.src.units.unit import Unit, CombinedUnit
from typing import Any, Callable


class Value:

    def __init__(self, value: Any, connected_interface: Any = None) -> None:
        self.__value = value
        self.__connected_interface = connected_interface

    def __hash__(self) -> str:
        return f"{self.__class__.__name__}{hash(self.value)}"

    @property
    def value(self) -> Any:
        return self.__value

    @property
    def connected_interface(self) -> Any:
        return self.__connected_interface


class NumberValue(Value):

    def __init__(
        self,
        value: float | Decimal | int,
        unit: Unit | CombinedUnit | None = None,
        decimal_places: int = 9,
        connected_interface: Any = None,
    ) -> None:
        try:
            value = Decimal(value).quantize(Decimal(f"1e-{decimal_places}"))
        except ValueError:
            raise ValueError(f"Invalid value for NumberValue: {value}")
        super().__init__(value=value, connected_interface=connected_interface)
        self.__decimal_places = decimal_places
        if (
            unit is not None
            and not isinstance(unit, Unit)
            and not isinstance(unit, CombinedUnit)
        ):
            raise TypeError(
                f"Invalid type for unit: {type(unit)}, must be Unit or CombinedUnit"
            )
        self.__unit = unit

    @property
    def decimal_places(self) -> int:
        return self.__decimal_places

    @property
    def unit(self) -> Unit | CombinedUnit | None:
        return self.__unit

    def convert(self, to_unit: Unit) -> NumberValue:
        if self.unit is None:
            raise ValueError("Cannot convert a unitless number")
        if isinstance(self.unit, CombinedUnit):
            combined_unit = self.unit.resetTotalFactor()
            new_unit = combined_unit.convert(to_unit)
            factor = new_unit.total_factor
        else:
            factor, new_unit = self.unit.convert(to_unit)
        return NumberValue(
            value=self.value * factor,
            unit=new_unit,
            decimal_places=self.decimal_places,
            connected_interface=self.connected_interface,
        )

    @classmethod
    def __cast(cls, value: Any, decimal_places: int = 9) -> NumberValue:
        if isinstance(value, NumberValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return NumberValue(value=value, decimal_places=decimal_places)

    def __mathOperation(
        self, other: NumberValue | int | float | str, operation: Callable
    ) -> NumberValue:
        other = self.__cast(other, decimal_places=self.decimal_places)
        return NumberValue(
            value=operation(self.value, other.value),
            decimal_places=max(self.decimal_places, other.decimal_places),
            connected_interface=None,
            unit=other.unit,
        )

    def __addAndSub(
        self, other: NumberValue | int | float | str, operation: Callable
    ) -> NumberValue:
        other = self.__cast(other, decimal_places=self.decimal_places)
        new_unit, factor = self.__syncUnitsAddAndSub(other)
        new_value = operation(self.value * factor, other.value)
        return NumberValue(
            value=new_value,
            decimal_places=max(self.decimal_places, other.decimal_places),
            connected_interface=None,
            unit=new_unit,
        )

    def __syncUnitsAddAndSub(
        self, other: NumberValue
    ) -> tuple[Unit | CombinedUnit | None, float]:
        if self.unit is None or self.unit.is_none:
            return other.unit, 1
        if other.unit is None or other.unit.is_none:
            return self.unit, 1
        if isinstance(self.unit, CombinedUnit):
            new_unit = self.unit.resetTotalFactor().convert(other.unit)
            if new_unit != other.unit:
                raise ValueError("Cannot add or subtract different units")
            factor = new_unit.total_factor
        elif isinstance(other.unit, CombinedUnit):
            new_unit = other.unit.resetTotalFactor().convert(self.unit)
            if new_unit != self.unit:
                raise ValueError("Cannot add or subtract different units")
            factor = new_unit.total_factor
        else:
            factor, new_unit = self.unit.convert(other.unit)
        return new_unit, factor

    def __syncUnitsMulAndDiv(
        self, other: NumberValue, operation: Callable
    ) -> tuple[Unit | CombinedUnit | None, float]:
        if self.unit is None or self.unit.is_none:
            return other.unit, 1
        if other.unit is None or other.unit.is_none:
            return self.unit, 1
        new_unit: CombinedUnit = operation(self.unit, other.unit)
        return new_unit, new_unit.total_factor

    def __mulAndDiv(
        self, other: NumberValue | int | float | str, operation: Callable
    ) -> NumberValue:
        other = self.__cast(other, decimal_places=self.decimal_places)
        new_unit, factor = self.__syncUnitsMulAndDiv(other, operation)
        new_value = operation(self.value, other.value) * factor
        return NumberValue(
            value=new_value,
            decimal_places=max(self.decimal_places, other.decimal_places),
            connected_interface=None,
            unit=new_unit,
        )

    def __powOperation(
        self, other: NumberValue | int | float | str, operation: Callable
    ) -> NumberValue:
        if isinstance(other, NumberValue):
            if other.unit is not None and not other.unit.is_none:
                raise ValueError("Cannot raise a number to a unit")

        other = self.__cast(self, decimal_places=self.decimal_places)
        return NumberValue(
            value=operation(self.value, other.value),
            decimal_places=max(self.decimal_places, other.decimal_places),
            connected_interface=None,
            unit=self.unit,
        )

    def __boolOperation(
        self, other: NumberValue | int | float | str, operation: Callable
    ) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __add__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__addAndSub(other, lambda x, y: x + y)

    def __sub__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__addAndSub(other, lambda x, y: x - y)

    def __mul__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mulAndDiv(other, lambda x, y: x * y)

    def __truediv__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mulAndDiv(other, lambda x, y: x / y)

    def __floordiv__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mulAndDiv(other, lambda x, y: x // y)

    def __mod__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mulAndDiv(other, lambda x, y: x % y)

    def __pow__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__powOperation(other, lambda x, y: x**y)

    def __eq__(self, other: NumberValue | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: NumberValue | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __lt__(self, other: NumberValue | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x < y)

    def __le__(self, other: NumberValue | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x <= y)

    def __gt__(self, other: NumberValue | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x > y)

    def __ge__(self, other: NumberValue | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x >= y)

    def __and__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mathOperation(other, lambda x, y: x & y)

    def __or__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mathOperation(other, lambda x, y: x | y)

    def __xor__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mathOperation(other, lambda x, y: x ^ y)

    def __lshift__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mathOperation(other, lambda x, y: x << y)

    def __rshift__(self, other: NumberValue | int | float | str) -> NumberValue:
        return self.__mathOperation(other, lambda x, y: x >> y)

    def __neg__(self) -> NumberValue:
        return NumberValue(value=-self.value, decimal_places=self.decimal_places)

    def __pos__(self) -> NumberValue:
        return NumberValue(value=+self.value, decimal_places=self.decimal_places)

    def __abs__(self) -> NumberValue:
        return NumberValue(value=abs(self.value), decimal_places=self.decimal_places)

    def __invert__(self) -> NumberValue:
        return NumberValue(value=~self.value, decimal_places=self.decimal_places)

    def __round__(self, n: int = 0) -> NumberValue:
        return NumberValue(value=self.value, decimal_places=n)

    def __floor__(self) -> NumberValue:
        return NumberValue(value=int(self.value), decimal_places=0)

    def __ceil__(self) -> NumberValue:
        return NumberValue(value=int(self.value) + 1, decimal_places=0)

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"NumberValue({self.value})"


class StringValue(Value):

    def __init__(self, value: Any, connected_interface: Any = None) -> None:
        super().__init__(value=str(value), connected_interface=connected_interface)

    def __cast(self, value: Any) -> "StringValue":
        if isinstance(value, StringValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return StringValue(value=value)

    def __boolOperation(self, other: Any, operation: Callable) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __eq__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __lt__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x < y)

    def __le__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x <= y)

    def __gt__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x > y)

    def __ge__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x >= y)

    def __add__(self, other: Any) -> "StringValue":
        return StringValue(value=self.value + self.__cast(other).value)

    def __mul__(self, other: int) -> "StringValue":
        return StringValue(value=self.value * other)

    def __rmul__(self, other: int) -> "StringValue":
        return self.__mul__(other)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"StringValue({self.value})"

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __len__(self) -> int:
        return len(self.value)


class BooleanValue(Value):

    def __init__(self, value: Any, connected_interface: Any = None) -> None:
        super().__init__(value=bool(value), connected_interface=connected_interface)

    def __cast(self, value: Any) -> "BooleanValue":
        if isinstance(value, BooleanValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return BooleanValue(value=value)

    def __boolOperation(self, other: Any, operation: Callable) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __eq__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __and__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x and y)

    def __or__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x or y)

    def __xor__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x ^ y)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"BooleanValue({self.value})"

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __invert__(self) -> bool:
        return not self.value

    def __index__(self) -> int:
        return int(self.value)

    def __bool__(self) -> bool:
        return self.value


class DateValue(Value):

    def __init__(
        self, value: str | datetime | date, connected_interface: Any = None
    ) -> None:
        if isinstance(value, str):
            value = datetime.fromisoformat(value).date()
        elif isinstance(value, datetime):
            value = value.date()
        elif not isinstance(value, date):
            raise ValueError(f"Invalid value for DateValue: {value}")
        super().__init__(value=value, connected_interface=connected_interface)

    def __cast(self, value: Any) -> "DateValue":
        if isinstance(value, DateValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return DateValue(value=value)

    def __boolOperation(self, other: Any, operation: Callable) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __mathOperation(self, other: Any, operation: Callable) -> "DateValue":
        if isinstance(other, timedelta):
            return DateValue(value=operation(self.value, other))
        return DateValue(value=operation(self.value, self.__cast(other).value))

    def __eq__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __lt__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x < y)

    def __le__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x <= y)

    def __gt__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x > y)

    def __ge__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x >= y)

    def __add__(self, other: Any) -> DateValue:
        return self.__mathOperation(other, lambda x, y: x + y)

    def __sub__(self, other: Any) -> DateValue | timedelta:
        return self.__mathOperation(other, lambda x, y: x - y)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"DateValue({self.value})"

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __bool__(self) -> bool:
        return bool(self.value)


class DateTimeValue(Value):

    def __init__(
        self, value: str | datetime | date, connected_interface: Any = None
    ) -> None:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        elif isinstance(value, date):
            value = datetime.combine(value, datetime.min.time())
        elif not isinstance(value, datetime):
            raise ValueError(f"Invalid value for DateTimeValue: {value}")
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        super().__init__(value=value, connected_interface=connected_interface)

    def __cast(self, value: Any) -> "DateTimeValue":
        if isinstance(value, DateTimeValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return DateTimeValue(value=value)

    def __boolOperation(self, other: Any, operation: Callable) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __mathOperation(self, other: Any, operation: Callable) -> "DateTimeValue":
        if isinstance(other, timedelta):
            return DateTimeValue(value=operation(self.value, other))
        return DateTimeValue(value=operation(self.value, self.__cast(other).value))

    def __eq__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __lt__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x < y)

    def __le__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x <= y)

    def __gt__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x > y)

    def __ge__(self, other: Any) -> bool:
        return self.__boolOperation(other, lambda x, y: x >= y)

    def __add__(self, other: Any) -> "DateTimeValue":
        return self.__mathOperation(other, lambda x, y: x + y)

    def __sub__(self, other: Any) -> "DateTimeValue":
        return self.__mathOperation(other, lambda x, y: x - y)

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"DateTimeValue({self.value})"

    def __int__(self) -> int:
        return int(self.value.timestamp())

    def __float__(self) -> float:
        return float(self.value.timestamp())

    def __bool__(self) -> bool:
        return bool(self.value)
