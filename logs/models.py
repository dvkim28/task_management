from django.db import models

from accounts.models import User
from projects.models import Task, Project


class Log(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-timestamp']
