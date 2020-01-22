from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        UserManager)

from account.lfb_account.querysets import AccountQuerySet
from core.behaviors import Timestampable, Operatable


class User(Timestampable,
           Operatable,
           AbstractBaseUser,
           PermissionsMixin):
    """系统用户信息表
        继承django最基本User Model
    """

    DISPLAY_FIELDS = ('username', 'last_login', 'created',
                      'modified', 'id')
    USERNAME_FIELD = 'username'
    RENAMED_FIELD = 'username'

    id = models.AutoField(
        primary_key=True,
        editable=False)
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='用户名')
    email = models.CharField(
        max_length=300,
        unique=True,
        null=True,
        blank=True,
        verbose_name='邮件地址')
    phone = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name='电话号码')

    objects = UserManager()
    object_list = AccountQuerySet.as_manager()

    class Meta(AbstractBaseUser.Meta):
        managed = False
        db_table = 'lfb_user'
        get_latest_by = '-modified'
        ordering = ['-created']
        indexes = [models.Index(fields=['username'])]
        verbose_name = '用户信息表'

    def __str__(self):
        return self.username
