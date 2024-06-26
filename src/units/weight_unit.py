from DataBucket.src.units.unit import Unit


class WeightUnit(Unit):

    @classmethod
    def initialize_class(cls):
        cls.MILLIGRAM = WeightUnit("Milligram", "mg")
        cls.GRAM = WeightUnit("Gram", "g")
        cls.KILOGRAM = WeightUnit("Kilogram", "kg")
        cls.TONNE = WeightUnit("Tonne", "t")
        cls.POUND = WeightUnit("Pound", "lb")
        cls.OUNCE = WeightUnit("Ounce", "oz")

        cls.FACTOR_DICT = {
            cls.MILLIGRAM: 1e-6,
            cls.GRAM: 1e-3,
            cls.KILOGRAM: 1,
            cls.TONNE: 1e3,
            cls.POUND: 0.45359237,
            cls.OUNCE: 0.028349523125,
        }

        cls.DB_BASE_UNIT = cls.KILOGRAM


WeightUnit.initialize_class()
