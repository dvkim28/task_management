from django.db import models

from accounts.models import User


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    crew = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='creator')
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    is_done = models.BooleanField(default=False)
    priorities = [
        ("Low", 'Low'),
        ("Medium", 'Medium'),
        ("High", 'High'),
        ("Critical", 'Critical'),
    ]
    priority = models.CharField(choices=priorities, default="Low", max_length=100)
    assigned_to = models.ForeignKey(User,
                                    blank=True,
                                    null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='assigned_to')
    task_type = models.ForeignKey(TaskType,
                                  on_delete=models.CASCADE,
                                  related_name='task_type')
    projects = models.ForeignKey(Project,
                                 on_delete=models.CASCADE)
    statuses = [
        ("To do", 'To do'),
        ("In progress", 'In progress'),
        ("In test", 'In test'),
        ("Done", 'Done'),
    ]
    status = models.CharField(
        choices=statuses,
        default="To do",
        max_length=100)

    def __str__(self):
        return self.title

    def formatted_date(self):
        return self.deadline.strftime("%d/%m/%Y")


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    def __str__(self):
        return f"Comment from {self.author} at {self.created_at}| project {self.task.projects}"