# -*- coding: utf-8 -*-
# @Time    : 2020/10/22 11:29
# @Author  : Fighter
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y