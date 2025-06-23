from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoDev03.settings') # 项目的settings文件

app = Celery('AutoTest') # 项目名为入参

app.config_from_object('django.conf:settings') # 读取settings中的celery配置

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)