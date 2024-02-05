from task.models import TodoTaskModel
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoTaskModel
        fields = ["id", "title", "description", "completed"]