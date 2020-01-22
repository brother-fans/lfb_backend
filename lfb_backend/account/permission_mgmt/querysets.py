from django.db.models import QuerySet

from core.querysets import CRUDQuerySet, DisplayQuerySet, FilterQuerySet


class PermissionQuerySet(DisplayQuerySet,
                         CRUDQuerySet,
                         FilterQuerySet,
                         QuerySet):
    pass


class RoleQuerySet(DisplayQuerySet, CRUDQuerySet, FilterQuerySet, QuerySet):
    pass
