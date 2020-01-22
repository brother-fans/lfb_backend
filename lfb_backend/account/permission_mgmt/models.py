from django.db import models

from core.behaviors import (Informable, Modifiable, Operatable, Timestampable,
                            SoftDeletable)

from .querysets import PermissionQuerySet, RoleQuerySet


class Permission(Informable,
                 Modifiable,
                 Operatable,
                 SoftDeletable,
                 Timestampable,
                 models.Model):

    DISPLAY_FIELDS = ('name', 'modifer', 'operator', 'created', 'modified',
                      'id', 'displayed', 'editable')
    RENAME_FIELD = 'name'

    id = models.AutoField(
        primary_key=True,
        editale=False,
        verbose_name='唯一标识')
    displayed = models.BooleanField(
        default=True,
        verbose_name='是否展示')
    is_private = models.BooleanField(
        default=True,
        verbose_name='是否私有',
        help_text='用于判断是否应用于所有角色')
    editable = models.CharField(
        default=True,
        verbose_name='是否允许编辑',
        help_text='是否允许对权限进行编辑')
    interface = models.CharField(
        max_length=500,
        verbose_name='接口url')

    objects = models.Manager()
    object_list = PermissionQuerySet.as_manager()

    class Meta:
        managed = True
        db_table = 'lfb_permission'
        get_latest_by = '-created'
        ordering = ['created']
        verbose_name = '权限信息表'

    def __str__(self):
        return self.name


class Role(Informable,
           Modifiable,
           Operatable,
           SoftDeletable,
           Timestampable,
           models.Model):

    DISPLAY_FIELDS = ('name', 'modifier', 'operator', 'created', 'modified',
                      'id')
    RENAME_FIELD = 'name'

    id = models.AutoField(
        primary_key=True,
        editable=False,
        verbose_name='唯一标识')
    permission = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='role_list',
        verbose_name='权限列表',
        db_table='lfb_role_permission')

    objects = models.Manager()
    object_list = RoleQuerySet.as_manager()

    class Meta:
        managed = True
        db_table = 'lfb_role'
        get_lastest_by = '-created'
        ordering = ['created']
        verbose_name = '角色信息表'

    def __str__(self):
        return self.name
