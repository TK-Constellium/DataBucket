from __future__ import annotations
from DataBucket.src.units.unit import Unit
from datetime import datetime, timezone
from typing import Callable


def getCurrentUnitFactorFunction(lamda_function: Callable | None = None) -> Callable:
    def NotImplemented(unit: CurrencyUnit, datetime: datetime) -> float:
        raise NotImplementedError

    if lamda_function is None:
        return NotImplemented
    return lamda_function


class CurrencyUnit(Unit):

    date: Callable = lambda: datetime.now(tz=timezone.utc)

    @classmethod
    def initialize_class(cls):
        cls.USD = cls("US Dollar", "USD")
        cls.EUR = cls("Euro", "EUR")
        cls.GBP = cls("British Pound", "GBP")
        cls.JPY = cls("Japanese Yen", "JPY")
        cls.CNY = cls("Chinese Yuan", "CNY")
        cls.AUD = cls("Australian Dollar", "AUD")
        cls.CAD = cls("Canadian Dollar", "CAD")
        cls.CHF = cls("Swiss Franc", "CHF")
        cls.SEK = cls("Swedish Krona", "SEK")
        cls.NZD = cls("New Zealand Dollar", "NZD")

        cls.FACTOR_DICT = {
            cls.USD: cls.__getCurrentFactor(cls.USD),
            cls.EUR: cls.__getCurrentFactor(cls.EUR),
            cls.GBP: cls.__getCurrentFactor(cls.GBP),
            cls.JPY: cls.__getCurrentFactor(cls.JPY),
            cls.CNY: cls.__getCurrentFactor(cls.CNY),
            cls.AUD: cls.__getCurrentFactor(cls.AUD),
            cls.CAD: cls.__getCurrentFactor(cls.CAD),
            cls.CHF: cls.__getCurrentFactor(cls.CHF),
            cls.SEK: cls.__getCurrentFactor(cls.SEK),
            cls.NZD: cls.__getCurrentFactor(cls.NZD),
        }

        cls.DB_BASE_UNIT = cls.USD

    @classmethod
    def __getCurrentFactor(cls, unit: CurrencyUnit) -> float:
        default_factor_dict = {
            CurrencyUnit.USD: 1,
            CurrencyUnit.EUR: 1.21,
            CurrencyUnit.GBP: 1.39,
            CurrencyUnit.JPY: 0.0095,
            CurrencyUnit.CNY: 0.15,
            CurrencyUnit.AUD: 0.77,
            CurrencyUnit.CAD: 0.79,
            CurrencyUnit.CHF: 1.11,
            CurrencyUnit.SEK: 0.12,
            CurrencyUnit.NZD: 0.72,
        }
        try:
            return getCurrentUnitFactorFunction()(unit, cls.date())
        except NotImplementedError:
            return default_factor_dict[unit]
