from __future__ import annotations

from decimal import Decimal
from datetime import date, datetime, timedelta
from typing import Union


class Value:

    def __init__(self, value: any, connected_interface: any = None) -> None:
        self.__value = value
        self.__connected_interface = connected_interface

    def __hash__(self) -> int:
        return f"{self.__class__.__name__}{hash(self.value)}"

    @property
    def value(self) -> any:
        return self.__value

    @property
    def connected_interface(self) -> any:
        return self.__connected_interface


class NumberValue(Value):

    def __init__(
        self,
        value: float | Decimal | int,
        decimal_places: int = 9,
        connected_interface: any = None,
    ) -> None:
        try:
            value = Decimal(value).quantize(Decimal(f"1e-{decimal_places}"))
        except ValueError:
            raise ValueError(f"Invalid value for NumberValue: {value}")
        super().__init__(value=value, connected_interface=connected_interface)
        self.__decimal_places = decimal_places

    @property
    def decimal_places(self) -> int:
        return self.__decimal_places

    @classmethod
    def __cast(cls, value: any, decimal_places: int = 9) -> "NumberValue":
        if isinstance(value, NumberValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return NumberValue(value=value, decimal_places=decimal_places)

    def __mathOperation(
        self, other: "NumberValue" | int | float | str, operation: callable
    ) -> "NumberValue":
        other = self.__cast(other, decimal_places=self.decimal_places)
        return NumberValue(
            value=operation(self.value, other.value),
            decimal_places=max(self.decimal_places, other.decimal_places),
            connected_interface=None,
        )

    def __boolOperation(
        self, other: "NumberValue" | int | float | str, operation: callable
    ) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __add__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x + y)

    def __sub__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x - y)

    def __mul__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x * y)

    def __truediv__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x / y)

    def __floordiv__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x // y)

    def __mod__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x % y)

    def __pow__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x**y)

    def __eq__(self, other: "NumberValue" | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: "NumberValue" | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __lt__(self, other: "NumberValue" | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x < y)

    def __le__(self, other: "NumberValue" | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x <= y)

    def __gt__(self, other: "NumberValue" | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x > y)

    def __ge__(self, other: "NumberValue" | int | float | str) -> bool:
        return self.__boolOperation(other, lambda x, y: x >= y)

    def __and__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x & y)

    def __or__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x | y)

    def __xor__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x ^ y)

    def __lshift__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x << y)

    def __rshift__(self, other: "NumberValue" | int | float | str) -> "NumberValue":
        return self.__mathOperation(other, lambda x, y: x >> y)

    def __neg__(self) -> "NumberValue":
        return NumberValue(value=-self.value, decimal_places=self.decimal_places)

    def __pos__(self) -> "NumberValue":
        return NumberValue(value=+self.value, decimal_places=self.decimal_places)

    def __abs__(self) -> "NumberValue":
        return NumberValue(value=abs(self.value), decimal_places=self.decimal_places)

    def __invert__(self) -> "NumberValue":
        return NumberValue(value=~self.value, decimal_places=self.decimal_places)

    def __round__(self, n: int = 0) -> "NumberValue":
        return NumberValue(value=self.value, decimal_places=n)

    def __floor__(self) -> "NumberValue":
        return NumberValue(value=int(self.value), decimal_places=0)

    def __ceil__(self) -> "NumberValue":
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

    def __init__(self, value: any, connected_interface: any = None) -> None:
        super().__init__(value=str(value), connected_interface=connected_interface)

    def __cast(self, value: any) -> "StringValue":
        if isinstance(value, StringValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return StringValue(value=value)

    def __boolOperation(self, other: any, operation: callable) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __eq__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __lt__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x < y)

    def __le__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x <= y)

    def __gt__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x > y)

    def __ge__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x >= y)

    def __add__(self, other: any) -> "StringValue":
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

    def __init__(self, value: any, connected_interface: any = None) -> None:
        super().__init__(value=bool(value), connected_interface=connected_interface)

    def __cast(self, value: any) -> "BooleanValue":
        if isinstance(value, BooleanValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return BooleanValue(value=value)

    def __boolOperation(self, other: any, operation: callable) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __eq__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __and__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x and y)

    def __or__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x or y)

    def __xor__(self, other: any) -> bool:
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

    def __init__(self, value: any, connected_interface: any = None) -> None:
        if isinstance(value, str):
            value = datetime.fromisoformat(value).date()
        try:
            value = date(value)
        except ValueError:
            raise ValueError(f"Invalid value for DateValue: {value}")
        super().__init__(value=value, connected_interface=connected_interface)

    def __cast(self, value: any) -> "DateValue":
        if isinstance(value, DateValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return DateValue(value=value)

    def __boolOperation(self, other: any, operation: callable) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __mathOperation(self, other: any, operation: callable) -> "DateValue":
        if isinstance(other, timedelta):
            return DateValue(value=operation(self.value, other))
        return DateValue(value=operation(self.value, self.__cast(other).value))

    def __eq__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __lt__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x < y)

    def __le__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x <= y)

    def __gt__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x > y)

    def __ge__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x >= y)

    def __add__(self, other: any) -> "DateValue":
        return self.__mathOperation(other, lambda x, y: x + y)

    def __sub__(self, other: any) -> "DateValue" | timedelta:
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

    def __init__(self, value: any, connected_interface: any = None) -> None:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        try:
            value = datetime(value)
        except ValueError:
            raise ValueError(f"Invalid value for DateTimeValue: {value}")
        super().__init__(value=value, connected_interface=connected_interface)

    def __cast(self, value: any) -> "DateTimeValue":
        if isinstance(value, DateTimeValue):
            return value
        if isinstance(value, Value):
            value = value.value
        return DateTimeValue(value=value)

    def __boolOperation(self, other: any, operation: callable) -> bool:
        return operation(self.value, self.__cast(other).value)

    def __mathOperation(self, other: any, operation: callable) -> "DateTimeValue":
        if isinstance(other, timedelta):
            return DateTimeValue(value=operation(self.value, other))
        return DateTimeValue(value=operation(self.value, self.__cast(other).value))

    def __eq__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x == y)

    def __ne__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x != y)

    def __lt__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x < y)

    def __le__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x <= y)

    def __gt__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x > y)

    def __ge__(self, other: any) -> bool:
        return self.__boolOperation(other, lambda x, y: x >= y)

    def __add__(self, other: any) -> "DateTimeValue":
        return self.__mathOperation(other, lambda x, y: x + y)

    def __sub__(self, other: any) -> "DateTimeValue":
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
