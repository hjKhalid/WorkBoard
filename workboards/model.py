# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

class WorkBoard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Task(models.Model):
    STATUS_CHOICES = [('ToDo', 'ToDo'), ('In Progress', 'In Progress'), ('Completed', 'Completed')]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ToDo')
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    workboard = models.ForeignKey(WorkBoard, related_name='tasks', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Send an email when the task is assigned to a user
        if self.pk is None:  # If task is being created
            self.send_task_assigned_email()
        else:
            original_task = Task.objects.get(pk=self.pk)
            if original_task.assigned_user != self.assigned_user:
                self.send_task_assigned_email()
        super().save(*args, **kwargs)

    def send_task_assigned_email(self):
        if self.assigned_user:
            send_mail(
                subject='You have been assigned a new task',
                message=f'Hello {self.assigned_user.username}, you have been assigned the task "{self.title}".',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.assigned_user.email],
            )
