# consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Task, WorkBoard

class TaskConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'tasks'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'create_task':
            task_title = data['title']
            workboard_id = data['workboard_id']
            status = data.get('status', 'ToDo')

            workboard = WorkBoard.objects.get(id=workboard_id)
            task = Task.objects.create(title=task_title, workboard=workboard, status=status)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'task_created',
                    'task': {
                        'id': task.id,
                        'title': task.title,
                        'status': task.status,
                        'workboard_id': task.workboard.id,
                    }
                }
            )
        
        elif action == 'delete_task':
            task_id = data['task_id']
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'task_deleted',
                        'task_id': task_id
                    }
                )
            except Task.DoesNotExist:
                self.send(text_data=json.dumps({'error': 'Task not found'}))

    def task_created(self, event):
        task = event['task']
        self.send(text_data=json.dumps({'action': 'task_created', 'task': task}))

    def task_deleted(self, event):
        task_id = event['task_id']
        self.send(text_data=json.dumps({'action': 'task_deleted', 'task_id': task_id}))
