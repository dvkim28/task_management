from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from projects.models import Project, TaskType, Task, Comment


class TestModels(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="Test description",
        )
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        self.task = Task.objects.create(
            title="Test",
            projects=self.project,
            task_type=self.task_type,
            creator=self.user,
            created_at=timezone.now(),
            description="Test Description",
            deadline=timezone.now() + timezone.timedelta(days=1),
            priority="Low",
            assigned_to=self.user,
            status="To do",
        )
        self.comment = Comment.objects.create(
            author=self.user,
            task=self.task,
            created_at=timezone.now(),
            text="Test comment",
        )

    def test_project_str_method(self):
        self.assertEqual(str(self.project), self.project.name)

    def test_task_type_str_method(self):
        self.assertEqual(str(self.task_type), self.task_type.name)

    def test_task_str_method(self):
        self.assertEqual(str(self.task), self.task.title)

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment),
                         f"Comment from {self.comment.author} "
                         f"at {self.comment.created_at}|"
                         f" project {self.comment.task.projects}")
