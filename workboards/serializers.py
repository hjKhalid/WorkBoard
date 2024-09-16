# serializers.py
from rest_framework import serializers
from .model import WorkBoard, Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class WorkBoardSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = WorkBoard
        fields = '__all__'
