from DataBucket.src.units.unit import Unit, CombinedUnit
from DataBucket.src.units.length_unit import LengthUnit
from DataBucket.src.units.weight_unit import WeightUnit

from django.test import TestCase


class TestUnitConversions(TestCase):
    def test_length_conversion(self):
        self.assertEqual(
            LengthUnit.convert(LengthUnit.METER, LengthUnit.MILLIMETER)[0], 1000
        )
        self.assertEqual(
            LengthUnit.convert(LengthUnit.METER, LengthUnit.CENTIMETER)[0], 100
        )
        self.assertEqual(
            LengthUnit.convert(LengthUnit.METER, LengthUnit.KILOMETER)[0], 0.001
        )

        self.assertEqual(
            LengthUnit.convert(LengthUnit.MILLIMETER, LengthUnit.METER)[0], 0.001
        )
        self.assertEqual(
            LengthUnit.convert(LengthUnit.CENTIMETER, LengthUnit.METER)[0], 0.01
        )
        self.assertEqual(
            LengthUnit.convert(LengthUnit.KILOMETER, LengthUnit.METER)[0], 1000
        )

    def test_weight_conversion(self):
        self.assertEqual(
            WeightUnit.convert(WeightUnit.GRAM, WeightUnit.KILOGRAM)[0], 0.001
        )
        self.assertEqual(WeightUnit.convert(WeightUnit.GRAM, WeightUnit.TON)[0], 1e-6)
        self.assertEqual(
            WeightUnit.convert(WeightUnit.KILOGRAM, WeightUnit.GRAM)[0], 1000
        )
        self.assertEqual(WeightUnit.convert(WeightUnit.TON, WeightUnit.GRAM)[0], 1e6)

    def test_combined_unit(self):
        a = CombinedUnit([WeightUnit.GRAM], [LengthUnit.METER])
        b = a.convertUnit(WeightUnit.KILOGRAM)
        c = b / LengthUnit.METER
        d = c * LengthUnit.METER * LengthUnit.METER

        self.assertEqual(a.total_factor, 1)
        self.assertEqual(a.numerator, [WeightUnit.GRAM])
        self.assertEqual(a.denominator, [LengthUnit.METER])

        self.assertEqual(b.total_factor, 0.001)
        self.assertEqual(b.numerator, [WeightUnit.KILOGRAM])
        self.assertEqual(b.denominator, [LengthUnit.METER])

        self.assertEqual(c.total_factor, 0.001)
        self.assertEqual(c.numerator, [WeightUnit.KILOGRAM])
        self.assertEqual(c.denominator, [LengthUnit.METER, LengthUnit.METER])

        self.assertEqual(d.total_factor, 0.001)
        self.assertEqual(d.numerator, [WeightUnit.KILOGRAM])
        self.assertEqual(d.denominator, [])
