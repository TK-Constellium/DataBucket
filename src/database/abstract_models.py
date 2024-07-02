from django.conf import settings
from django.db import models


class unchangeable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @property
    def get_current_changeable(self):
        return self.__link_to_unchangeable_set.all().last()  # type: ignore


class changeable(models.Model):
    __link_to_unchangeable: models.ForeignKey
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @property
    def get_current_unchangeable(self):
        return self.__link_to_unchangeable
