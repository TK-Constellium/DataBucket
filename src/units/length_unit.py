from DataBucket.src.units.unit import Unit


class LengthUnit(Unit):

    @classmethod
    def initialize_class(cls):
        cls.NANOMETER = cls("Nanometer", "nm")
        cls.MILLIMETER = cls("Millimeter", "mm")
        cls.CENTIMETER = cls("Centimeter", "cm")
        cls.METER = cls("Meter", "m")
        cls.KILOMETER = cls("Kilometer", "km")
        cls.INCH = cls("Inch", "in")
        cls.FOOT = cls("Foot", "ft")
        cls.YARD = cls("Yard", "yd")
        cls.MILE = cls("Mile", "mi")

        cls.FACTOR_DICT = {
            cls.NANOMETER: 1e-9,
            cls.MILLIMETER: 1e-3,
            cls.CENTIMETER: 1e-2,
            cls.METER: 1,
            cls.KILOMETER: 1e3,
            cls.INCH: 0.0254,
            cls.FOOT: 0.3048,
            cls.YARD: 0.9144,
            cls.MILE: 1609.344,
        }

        cls.DB_BASE_UNIT = cls.MILLIMETER


LengthUnit.initialize_class()
