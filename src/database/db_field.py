from __future__ import annotations

from django.db import models
from DataBucket.src.units.unit import Unit
from typing import Any


class dbField:

    IS_CHANGEABLE: bool = True
    IS_REQUIRED: bool = False
    IS_UNIQUE: bool = False
    DEFAULT: Any = None

    unit: Unit | None
    decimal_places: int | None
    max_length: int | None
    DataBucket: str | None
    related_name: str | None

    def __init__(self, **kwargs: dict[str, Any]):
        self.__is_changeable = self.__checkAndGetBool(
            kwargs, "is_changeable", self.IS_CHANGEABLE
        )
        self.__is_required = self.__checkAndGetBool(
            kwargs, "is_required", self.IS_REQUIRED
        )
        self.__is_unique = self.__checkAndGetBool(kwargs, "is_unique", self.IS_UNIQUE)
        self.__default: Any = kwargs.get("default", self.DEFAULT)

    def __checkAndGetBool(
        self, dict_data: dict[str, Any], name: str, default: bool
    ) -> bool:
        value = dict_data.get(name, default)
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be a boolean")
        return value

    @property
    def is_changeable(self) -> bool:
        return self.__is_changeable

    @property
    def is_required(self) -> bool:
        return self.__is_required

    @property
    def is_unique(self) -> bool:
        return self.__is_unique

    @property
    def default(self) -> Any:
        return self.__default

    @property
    def field(self) -> models.Field:
        raise NotImplementedError

    def DO_NOTHING(self):
        if not isinstance(self, DataBucketConnection):
            raise ValueError("CASCADE is only valid for DataBucketConnection")
        return

    def CASCADE(self):
        if not isinstance(self, DataBucketConnection):
            raise ValueError("CASCADE is only valid for DataBucketConnection")
        raise NotImplementedError
        # TODO: Implement CASCADE


class String(dbField):

    TYPE_CHOICES_DICT = {
        "ForeignKey": models.CharField,
        "ManyToMany": models.ManyToManyField,
    }

    def __init__(self, max_length: int = 256, **kwargs: dict):
        self.__max_length = max_length

        if max_length < 1:
            raise ValueError("max_length must be greater than 0")
        elif max_length > 255:
            self.field_representation = models.TextField
        else:
            self.field_representation = models.CharField
        super().__init__(**kwargs)

        attributes = {
            "max_length": self.max_length,
            "default": self.default,
        }
        if not self.is_required:
            attributes["null"] = True
        self.__field = self.field_representation(**attributes)

    @property
    def max_length(self) -> int:
        return self.__max_length

    @property
    def field(self) -> models.Field:
        return self.__field


class DataBucketConnection(dbField):

    TYPE_CHOICES_DICT = {
        "ForeignKey": models.ForeignKey,
        "OneToOne": models.OneToOneField,
        "ManyToMany": models.ManyToManyField,
    }

    def __init__(self, DataBucket: str, type: str, on_delete: dbField, **kwargs: dict):
        self.__DataBucket = DataBucket
        self.__type = type
        self.__on_delete = on_delete

        if type not in self.TYPE_CHOICES_DICT:
            raise ValueError(f"Invalid type: {type}")

        self.field_representation = self.TYPE_CHOICES_DICT[type]
        attributes = self.getFieldAttributes(type)

        super().__init__(**kwargs)

        self.__field = self.field_representation(
            self.__getDataBucketModelByName(self.DataBucket),
            **attributes,
        )

    def getFieldAttributes(self, type):
        attributes = {}
        if type != "ManyToMany":

            attributes["on_delete"] = models.DO_NOTHING
            attributes["null"] = not self.is_required

        return attributes

    @property
    def DataBucket(self) -> str:
        return self.__DataBucket

    @property
    def type(self) -> str:
        return self.__type

    @property
    def on_delete(self) -> dbField:
        return self.__on_delete

    @property
    def field(self) -> models.Field:
        return self.__field

    def __getDataBucketModelByName(self, name: str) -> models.Model:
        from DataBucket.src.database.database_interface import Database

        for subclass in Database.__subclasses__():
            if subclass.__name__ == f"{name}__unchangeable__" and issubclass(
                subclass, models.Model
            ):
                return subclass
        raise ValueError(f"DataBucket '{name}' not found")


class Number(dbField):
    MAX_DIGITS = 24
    DB_DECIAML_PLACES = 9

    def __init__(self, decimal_places: int, unit: Unit | None, **kwargs: dict):
        self.__decimal_places = decimal_places
        self.__unit = unit

        super().__init__(**kwargs)

        if decimal_places < 0:
            raise ValueError("decimal_places must be greater than or equal to 0")
        elif decimal_places > self.DB_DECIAML_PLACES:
            raise ValueError(
                f"decimal_places must be less than or equal to {self.DB_DECIAML_PLACES}"
            )

        attributes = {
            "max_digits": self.MAX_DIGITS,
            "decimal_places": self.DB_DECIAML_PLACES,
            "default": self.default,
        }
        if not self.is_required:
            attributes["null"] = True
        self.__field = models.DecimalField(**attributes)

    @property
    def decimal_places(self) -> int:
        return self.__decimal_places

    @property
    def unit(self) -> Unit | None:
        return self.__unit

    @property
    def field(self) -> models.Field:
        return self.__field
