from DataBucket.src.units.unit import Unit


class TimeUnit(Unit):

    @classmethod
    def initialize_class(cls):
        cls.NANOSECOND = cls("Nanosecond", "ns")
        cls.MICROSECOND = cls("Microsecond", "µs")
        cls.MILLISECOND = cls("Millisecond", "ms")
        cls.SECOND = cls("Second", "s")
        cls.MINUTE = cls("Minute", "min")
        cls.HOUR = cls("Hour", "h")
        cls.DAY = cls("Day", "d")
        cls.WEEK = cls("Week", "w")
        cls.MONTH = cls("Month", "mo")
        cls.YEAR = cls("Year", "y")

        cls.FACTOR_DICT = {
            cls.NANOSECOND: 1e-9,
            cls.MICROSECOND: 1e-6,
            cls.MILLISECOND: 1e-3,
            cls.SECOND: 1,
            cls.MINUTE: 60,
            cls.HOUR: 3600,
            cls.DAY: 86400,
            cls.WEEK: 604800,
            cls.MONTH: 2628000,
            cls.YEAR: 31536000,
        }

        cls.DB_BASE_UNIT = cls.SECOND


TimeUnit.initialize_class()
