from django.db.models import QuerySet

from core.querysets import (
    DisplayQuerySet,
    CRUDQuerySet,
    DateTimeQuerySet,
    FilterQuerySet)


class AccountQuerySet(DateTimeQuerySet,
                      DisplayQuerySet,
                      CRUDQuerySet,
                      FilterQuerySet,
                      QuerySet):
    pass
