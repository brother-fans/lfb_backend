"""app通用behaviors
"""

from django.db import models


class Timestampable(models.Model):
    """添加日期行为
    """

    created = models.DateTimeField(
        auto_now_add=True,
        editable=True,
        verbose_name='创建时间',
        help_text='YYYY-MM-DD hh:mm:ss format')
    modified = models.DateTimeField(
        auto_now=True,
        editable=True,
        verbose_name='修改时间',
        help_text='YYYY-MM-DD hh:mm:ss format')

    class Meta:
        abstract = True


class Informable(models.Model):
    """添加描述信息行为
    """

    name = models.CharField(
        max_length=100,
        verbose_name='名称',
        help_text='中文/英文')
    desc = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name='描述',
        help_text='中文/英文')

    class Meta:
        abstract = True


class Operatable(models.Model):
    """添加创建者行为
    """

    operator = models.CharField(
        max_length=50,
        verbose_name='创建者用户名',
        help_text='用户名')

    class Meta:
        abstract = True


class SoftDeletable(models.Model):
    """添加删除行为
    """

    is_deleted = models.BooleanField(
        default=False,
        verbose_name='删除标记',
        help_text='是否标记为删除(软删除功能)')

    class Meta:
        abstract = True
        
        
class Modifiable(models.Model):
    """添加修改者信息行为"""

    modifier = models.CharField(
        max_length=50,
        verbose_name='记录修改者用户名',
        help_text='用户名')
