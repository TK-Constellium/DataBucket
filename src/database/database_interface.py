from __future__ import annotations

from DataBucket.src.database.abstract_models import unchangeable, changeable
from DataBucket.src.auxiliary.interface_definition import (
    DataInterface,
    FieldInformationDict,
)
from DataBucket.src.database.db_field import dbField, Number
from django.apps import apps
from django.db import models
import os
import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from DataBucket.src.units.unit import Unit
    from DataBucket.src.data_bucket import DataBucket


class Database(DataInterface):
    data_bucket: DataBucket

    def getFields(self) -> list[FieldInformationDict]:
        return [
            FieldInformationDict(
                field_name=field_name,
                field_type=field.field.__class__.__name__,
                unit=field.unit if hasattr(field, "unit") else None,
                is_required=field.is_required,
                is_changeable=field.is_changeable,
                is_unique=field.is_unique,
                default=field.default,
                decimal_places=(
                    field.decimal_places if hasattr(field, "decimal_places") else None
                ),
                max_length=field.max_length if hasattr(field, "max_length") else None,
                connected_interface=(
                    field.DataBucket if hasattr(field, "DataBucket") else None
                ),
            )
            for field_name, field in self.__getFields().items()
        ]

    @classmethod
    def initialize_class(cls):
        defined_fields = cls.__getFields()
        file_path = cls.__getFilePath()
        model_tuple = cls.__createModels(defined_fields)
        cls.model_tuple = model_tuple
        cls.__registerModels(model_tuple, file_path)

    @classmethod
    def __getFields(cls) -> dict[str, dbField]:
        return {
            key: value
            for key, value in cls.__dict__.items()
            if isinstance(value, dbField)
        }

    @classmethod
    def __getFilePath(cls) -> str:
        module_name = cls.__module__
        module = sys.modules[module_name]
        return getattr(module, "__file__")

    @classmethod
    def __createModels(
        cls, defined_fields: dict[str, dbField]
    ) -> tuple[unchangeable, changeable]:
        unchangeable_fields, changeable_fields = cls.__sortFields(defined_fields)
        unchangeable_model = cls.__createModel(unchangeable_fields, unchangeable)
        changeable_model = cls.__createModel(changeable_fields, changeable)
        changeable_model.__link_to_unchangeable = models.ForeignKey(
            unchangeable_model, on_delete=models.CASCADE
        )
        return unchangeable_model, changeable_model

    @classmethod
    def __sortFields(cls, defined_fields: dict[str, dbField]) -> tuple[dict, dict]:
        unchangeable_fields = {}
        changeable_fields = {}
        for field_name, field in defined_fields.items():
            if isinstance(field, Number) and field.unit is not None:
                field.related_name = f"{field_name}_{field.unit.name}"
            if field.is_changeable:
                changeable_fields[field_name] = field
            else:
                unchangeable_fields[field_name] = field

        return unchangeable_fields, changeable_fields

    @classmethod
    def __createModel(
        cls,
        fields: dict[str, dbField],
        model_base: type[unchangeable] | type[changeable],
    ) -> unchangeable | changeable:
        attributes = {field_name: field.field for field_name, field in fields.items()}
        attributes["__module__"] = cls.__module__.split(".")[0]
        class_name = f"{cls.data_bucket.__name__}_{model_base.__name__}"
        model_class = type(class_name, (model_base,), attributes)
        return model_class

    @classmethod
    def __registerModels(
        cls, model_tuple: tuple[unchangeable, changeable], file_path: str
    ) -> None:
        app_label = cls.__getAppLabelFromFile(file_path)
        app_config = apps.get_app_config(app_label)
        for model_class in model_tuple:
            model_class._meta.app_label = app_label
            app_config.models[model_class.__name__.lower()] = model_class
            models.signals.class_prepared.send(sender=model_class)

    @staticmethod
    def __getAppLabelFromFile(file_path: str) -> str | None:
        abs_file_path = os.path.abspath(file_path)
        for app_config in apps.get_app_configs():
            app_path = os.path.abspath(app_config.path)
            if abs_file_path.startswith(app_path):
                return app_config.label
        return None
