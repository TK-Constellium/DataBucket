from DataBucket.src.units.unit import Unit


class WeightUnit(Unit):

    @classmethod
    def initialize_class(cls):
        cls.MILLIGRAM = cls("Milligram", "mg")
        cls.GRAM = cls("Gram", "g")
        cls.KILOGRAM = cls("Kilogram", "kg")
        cls.TON = cls("Ton", "t")
        cls.POUND = cls("Pound", "lb")
        cls.OUNCE = cls("Ounce", "oz")

        cls.FACTOR_DICT = {
            cls.MILLIGRAM: 1e-6,
            cls.GRAM: 1e-3,
            cls.KILOGRAM: 1,
            cls.TON: 1e3,
            cls.POUND: 0.45359237,
            cls.OUNCE: 0.028349523125,
        }

        cls.DB_BASE_UNIT = cls.KILOGRAM


WeightUnit.initialize_class()
