from __future__ import annotations

from DataBucket.src.units.unit import Unit
from dataclasses import dataclass
from typing import Any, Literal, TYPE_CHECKING

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

    @classmethod
    def _getInterfaceConnection(cls) -> DataInterface:
        raise NotImplementedError


class ConnectionType:
    pass


class ForeignKey(ConnectionType):
    pass


class ManyToMany(ConnectionType):
    pass


class OneToOne(ConnectionType):
    pass


class DataBucketConnection:

    CONNECTION_TYPE_TRANSLATION: dict[str, type[ConnectionType]] = {
        "ForeignKey": ForeignKey,
        "ManyToMany": ManyToMany,
        "OneToOne": OneToOne,
    }

    def __init__(
        self,
        data_bucket: type[DataBucket] | str,
        connection_type: Literal["ForeignKey", "ManyToMany", "OneToOne"],
        is_required: bool,
        on_delete: Any,
    ):
        self.__data_bucket = self.__getDataBucket(data_bucket)
        self.__connection_type = self.__getConnectionType(connection_type)
        self.__is_required = bool(is_required)
        self.__on_delete = on_delete

    def __getDataBucket(self, data_bucket: type[DataBucket] | str) -> type[DataBucket]:
        def getDataBucketByName(name: str) -> type[DataBucket]:
            for subclass in DataBucket.__subclasses__():
                if subclass.__name__ == name:
                    return subclass

            raise ValueError(f"DataBucket with name {name} not found")

        if isinstance(data_bucket, str):
            data_bucket = getDataBucketByName(data_bucket)
        if not issubclass(data_bucket, DataBucket):
            raise ValueError("data_bucket must be a subclass of DataBucket")
        return data_bucket

    def __getConnectionType(self, connection_type: str) -> type[ConnectionType]:
        if connection_type not in self.CONNECTION_TYPE_TRANSLATION:
            raise ValueError(
                f"connection_type must be one of {self.CONNECTION_TYPE_TRANSLATION.keys()}, not {connection_type}"
            )
        return self.CONNECTION_TYPE_TRANSLATION[connection_type]

    @property
    def data_bucket(self) -> type[DataBucket]:
        return self.__data_bucket

    @property
    def connection_type(self) -> type[ConnectionType]:
        return self.__connection_type

    @property
    def is_required(self) -> bool:
        return self.__is_required

    @property
    def on_delete(self) -> Any:
        return self.__on_delete
