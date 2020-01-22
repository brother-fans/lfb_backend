"""本地配置文件
    chenjunliang
"""

from .local import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'lfb_backend',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    },
    'mysql': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lfb_backend',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
}
