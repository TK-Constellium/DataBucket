from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataBucket.src.auxiliary.interface_definition import DataInterface


class DataBucket:

    objects: DataInterface
    DataInterface: DataInterface

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        if hasattr(cls, "DataInterface"):
            cls.DataInterface.data_bucket = cls()
            cls.DataInterface.initialize_class()
            cls.objects = cls.DataInterface


class DataBucketObject:
    def __init__(self, data_interface: DataInterface):
        self.data_interface = DataInterface

    def filter(self, filter: dict):
        return self.data_interface.filter(filter)

    def exclude(self, filter: dict):
        return self.data_interface.exclude(filter)

    def all(self):
        return self.data_interface.all()

    def create(self, data: dict):
        return self.data_interface.create(data)

    def delete(self, id: int):
        return self.data_interface.delete(id)

    def update(self, id: int, data: dict):
        return self.data_interface.update(id, data)

    def get(self, filter: dict):
        return self.filter(filter).first()


class DataBucketQuerryset:

    def __getitem__(self, item):
        return self[item]

    def first(self):
        return self[0]
