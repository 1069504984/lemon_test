from django.db import models
from djcelery.models import PeriodicTask
# Create your models here.
class TaskExtend(models.Model):
    """
    拓展PeriodicTask模型
    """
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    email_list = models.CharField('邮箱列表', max_length=2048, default='[]')
    author = models.CharField('创建人', max_length=100, default='')
    project = models.IntegerField('任务所选项目', default=0)
    periodic_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE, related_name='taskextend')