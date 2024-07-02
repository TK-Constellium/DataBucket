from __future__ import annotations

from DataBucket.src.units.unit import Unit
from dataclasses import dataclass
from typing import Any
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataBucket.src.data_bucket import (
        DataBucket,
        DataBucketObject,
        DataBucketQuerryset,
    )


@dataclass
class FieldInformationDict:
    field_name: str
    field_type: str
    decimal_places: int | None
    max_length: int | None
    connected_interface: str | None
    unit: Unit | None
    is_required: bool
    is_changeable: bool
    is_unique: bool
    default: Any


class DataInterface:
    data_bucket: DataBucket

    @classmethod
    def initialize_class(cls) -> None:
        raise NotImplementedError

    @classmethod
    def getFields(cls) -> FieldInformationDict:
        raise NotImplementedError

    @classmethod
    def all(cls) -> DataBucketQuerryset:
        raise NotImplementedError

    @classmethod
    def filter(cls, filter: dict) -> DataBucketQuerryset:
        raise NotImplementedError

    @classmethod
    def exclude(cls, filter: dict) -> DataBucketQuerryset:
        raise NotImplementedError

    @classmethod
    def create(cls, data: dict) -> DataBucketObject:
        raise NotImplementedError

    @classmethod
    def delete(cls, id: int) -> DataBucketObject:
        raise NotImplementedError

    @classmethod
    def update(cls, id: int, data: dict) -> DataBucketObject:
        raise NotImplementedError
