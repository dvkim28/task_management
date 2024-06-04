from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from logs.models import Log
from projects.models import Project, TaskType, Task


class PublicViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")

    def test_login_required(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 302)


class IndexViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='<EMAIL>',
            password='<PASSWORD>',
            username='testuser',
        )
        self.index_url = reverse("index")
        self.client.force_login(self.user)
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Project',
        )
        self.task_type_task = TaskType.objects.create(
            name='Test Task Type',
        )
        self.task_type_bug = TaskType.objects.create(
            name='Bug',
        )
        self.task = Task.objects.create(
            title='Test',
            projects=self.project,
            task_type=self.task_type_task,
            creator=self.user,
            created_at=timezone.now(),
            description='Test Description',
            deadline=timezone.now() + timezone.timedelta(days=1),
            priority="Low",
            assigned_to=self.user,
            status="To do",
        )
        self.bug = Task.objects.create(
            title='Test bug',
            projects=self.project,
            task_type=self.task_type_bug,
            creator=self.user,
            created_at=timezone.now(),
            description='Test Description',
            deadline=timezone.now() - timezone.timedelta(days=1),
            priority="Low",
            assigned_to=self.user,
            status="To do")
        self.log = Log.objects.create(
            user=self.user,
            timestamp=timezone.now(),
            action="Created",
            project=self.project,

        )
        self.response = self.client.get(self.index_url)

    def test_correctness_template(self):
        self.assertTemplateUsed(self.response, "pages/index.html")

    def test_expired_tasks_present(self):
        expired_tasks_count = Task.objects.filter(deadline__lte=timezone.now(), is_done=False).count()
        self.assertEqual(self.response.context["expired_tasks"].count(), expired_tasks_count)

    def test_percent_of_expired_tasks_present(self):
        tasks_count = Task.objects.filter(assigned_to=self.user).count()
        expired_tasks_count = Task.objects.filter(deadline__lte=timezone.now()).count()
        percent = round((expired_tasks_count / tasks_count) * 100)
        self.assertEqual(self.response.context["percent_of_expired_tasks"], percent)

    def test_bugs_present(self):
        bugs_count = Task.objects.filter(assigned_to=self.user,
                                         task_type=self.task_type_bug).count()
        self.assertEqual(self.response.context["bugs"].count(), bugs_count)

    def test_percent_of_bugs_present(self):
        bugs_count = Task.objects.filter(task_type=self.task_type_bug, assigned_to=self.user).count()
        tasks_count = Task.objects.filter(assigned_to=self.user).count()
        percent = round(bugs_count / tasks_count * 100)
        self.assertEqual(self.response.context["percent_of_bugs"], percent)

    def test_bugs_percentage_present(self):
        bugs = Task.objects.filter(task_type=self.task_type_bug)
        self.assertEqual(self.response.context["bugs"].count(), bugs.count())

    # def test_logs_present(self):
    #     expected_logs = [self.log]
    #
    #     self.assertEqual(list(self.response.context["logs"]), expected_logs)