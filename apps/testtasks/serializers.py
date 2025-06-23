from djcelery.models import PeriodicTask
from rest_framework import serializers
from testtasks.models import TaskExtend
from utils import validates

class TaskExtendSerializer(serializers.ModelSerializer):
    """
    任务拓展模块序列化
    """
    class Meta:
        model = TaskExtend
        fields = '__all__'

class PeriodicTaskSerializer(serializers.ModelSerializer):
    """
    用例信息序列化
    """
    task_extend = TaskExtendSerializer(source='taskextend', read_only=True)
    # crontab_time = CrontabScheduleSerializer(source='crontab', read_only=True)
    crontab_time = serializers.ReadOnlyField(source='crontab.__str__')
    class Meta:
        model = PeriodicTask
        fields = '__all__'