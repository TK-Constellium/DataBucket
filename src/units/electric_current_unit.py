from DataBucket.src.units.unit import Unit


class ElectricCurrentUnit(Unit):

    @classmethod
    def initialize_class(cls):
        cls.NANOAMPERE = cls("Nanoampere", "nA")
        cls.MICROAMPERE = cls("Microampere", "µA")
        cls.MILLIAMPERE = cls("Milliampere", "mA")
        cls.AMPERE = cls("Ampere", "A")
        cls.KILOAMPERE = cls("Kiloampere", "kA")
        cls.MEGAAMPERE = cls("Megaampere", "MA")

        cls.FACTOR_DICT = {
            cls.NANOAMPERE: 1e-9,
            cls.MICROAMPERE: 1e-6,
            cls.MILLIAMPERE: 1e-3,
            cls.AMPERE: 1,
            cls.KILOAMPERE: 1e3,
            cls.MEGAAMPERE: 1e6,
        }

        cls.DB_BASE_UNIT = cls.AMPERE


ElectricCurrentUnit.initialize_class()
