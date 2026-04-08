import uuid

from django.db import models

__all__ = ['TokenBase']


class TokenBase(models.Model):
    class Meta:
        abstract = True

    uid = models.UUIDField('UUID', default=uuid.uuid4)
    uid2 = models.UUIDField('UUID2', default=uuid.uuid4)

    expire = models.DateField('Истекает')

    usage_limit = models.PositiveSmallIntegerField('Лимит использований', default=5)
    current_usage = models.PositiveSmallIntegerField('Использован раз', default=0)

    def __str__(self):
        return f'{self.uid.hex} до {self.expire}'

    def get_absolute_url(self):
        raise NotImplementedError
