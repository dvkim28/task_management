from django.urls import reverse

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from logs.models import Log
from projects.forms import (FilterByMembersForm,
                            InviteNewMemberForm,
                            CreateTaskForm,
                            CommentForm)
from projects.models import Project, TaskType, Task, Comment


class PublicViewTests(TestCase):
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
        self.project_create = reverse("projects:project_create")
        self.project_detail = reverse("projects:project_detail",
                                      kwargs={"pk": self.project.pk})
        self.project_admin = reverse("projects:project_admin",
                                     kwargs={"pk": self.project.pk})
        self.task_create = reverse("projects:task_create")
        self.task_detail = reverse("projects:task_detail",
                                   kwargs={"pk": self.task.pk})
        self.task_list = reverse("projects:task-list", )

    def test_login_required(self):
        urls = [self.project_create,
                self.project_detail,
                self.project_admin,
                self.task_create,
                self.task_detail,
                self.task_list]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 500)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(response.url.startswith("/accounts/login/"))


class ProjectCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.client.force_login(self.user)

    def test_create_project(self):
        project = {
            "name": "Test Project",
            "description": "Test description",
        }
        url = reverse("projects:project_create")
        response = self.client.post(url, data=project)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        created_project = Project.objects.get(name="Test Project")
        self.assertTrue(created_project)
        self.assertTrue(self.user in created_project.managements.all())

    def test_correct_template(self):
        url = reverse("projects:project_create")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "pages/project-create.html")


class ProjectDetailViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.new_user = User.objects.create_user(
            username="invited_user",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.client.force_login(self.user)
        self.project = Project.objects.create(
            name="Test Project",
            description="Test description",
        )
        self.user.projects.add(self.project)
        self.url = reverse("projects:project_detail",
                           kwargs={"pk": self.project.pk})
        self.response = self.client.get(self.url)
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
            assigned_to=self.new_user,
            status="To do",
        )
        self.comment = Comment.objects.create(
            author=self.user,
            task=self.task,
            created_at=timezone.now(),
            text="Test comment",
        )

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/project_view.html")

    def test_project_members_presents(self):
        username = self.user.username
        self.assertContains(self.response, username)

    def test_filter_form_presents(self):
        form = FilterByMembersForm(data={"member": self.new_user})
        form.is_valid()
        self.assertEqual(form.cleaned_data, form.data)
        response = self.client.get(self.url)
        self.assertContains(response, self.new_user.username)
        self.assertContains(response, "<form")

class TaskCreateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.url = reverse("projects:task_create")
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        self.response = self.client.get(self.url)
        self.project = Project.objects.create(
            name="Test Project",
            description="Test description",
        )

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/task_form.html")

    def test_create_task_form(self):
        deadline = timezone.now().date() + timezone.timedelta(days=1)
        data = {
            "title": "Test Task",
            "description": "Test Description",
            "assigned_to": self.user,
            "deadline": deadline,
            "priority": "Low",
            "task_type": self.task_type.pk,
        }
        form = CreateTaskForm(data=data)
        form.is_valid()
        self.assertEqual(form.cleaned_data["title"], "Test Task")
        self.assertEqual(form.cleaned_data["description"], "Test Description")
        self.assertEqual(form.cleaned_data["assigned_to"], self.user)
        self.assertEqual(form.cleaned_data["deadline"], deadline)
        self.assertEqual(form.cleaned_data["priority"], "Low")
        self.assertEqual(form.cleaned_data["task_type"], self.task_type)

    def test_create_task(self):
        deadline = timezone.now().date() + timezone.timedelta(days=1)
        data = {
            "title": "Test Task",
            "description": "Test Description",
            "assigned_to": self.user.pk,
            "deadline": deadline,
            "priority": "Low",
            "task_type": self.task_type.pk,
            "projects": self.project.pk
        }
        self.client.post(self.url, data=data)
        task = Task.objects.last()
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.assigned_to, self.user)
        self.assertEqual(task.deadline, deadline)
        self.assertEqual(task.priority, "Low")
        self.assertEqual(task.task_type, self.task_type)
        self.assertEqual(task.projects, self.project)

    def test_create_task_with_log(self):
        data = {
            "title": "Test Task",
            "description": "Test Description",
            "assigned_to": self.user.pk,
            "deadline": "2024-06-14",
            "priority": "Low",
            "task_type": self.task_type.pk,
            "projects": self.project.pk,
        }

        response = self.client.post(reverse("projects:task_create"), data=data)

        self.assertEqual(response.status_code, 302)
        task = Task.objects.last()
        log = Log.objects.last()
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action, f"Created task: {task.title}")
        self.assertEqual(log.project, self.project)


class TaskDetailViewTests(TestCase):
    def setUp(self):
        self.new_user = User.objects.create_user(
            username="testuser2",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
        )
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        deadline = timezone.now().date() + timezone.timedelta(days=1)
        self.task = Task.objects.create(
            title="Test Task",
            projects=self.project,
            task_type=self.task_type,
            creator=self.user,
            deadline=deadline,
            created_at=timezone.now(),
            description="Test comment",
            assigned_to=self.user,
            status="Low"
        )
        self.url = reverse("projects:task_detail", kwargs={"pk": self.task.pk})
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/task-detail.html")

    def test_comment_form_with_logs(self):
        data = {
            "text": "Test comment",
        }
        self.client.post(self.url, data=data)
        comment = Comment.objects.last()
        self.assertEqual(comment.text, "Test comment")
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.task, self.task)
        log = Log.objects.last()
        self.assertEqual(log.action,
                         f"Added comment to the task: "
                         f"{self.task.title}")
        self.assertEqual(log.project, self.project)

    def test_general_form_presents_with_logs(self):
        deadline = timezone.now().date() + timezone.timedelta(days=2)
        data = {
            "deadline": deadline,
            "priority": "Medium",
            "assigned_to": self.new_user.pk,
            "status": "In progress",
        }
        self.client.post(self.url, data=data)
        self.task.refresh_from_db()
        self.assertEqual(self.task.priority, "Medium")
        self.assertEqual(self.task.assigned_to, self.new_user)
        self.assertEqual(self.task.deadline, deadline)
        log = Log.objects.last()
        self.assertEqual(log.action, f"Updated task: {self.task.title}")
        self.assertEqual(log.project, self.project)


class TaskListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="<EMAIL>",
            password="<PASSWORD>"
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description",
        )
        self.project2 = Project.objects.create(
            name="Test Project2",
            description="Test Description",
        )
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        deadline = timezone.now().date() + timezone.timedelta(days=1)
        self.task = Task.objects.create(
            title="Test Task",
            deadline=deadline,
            projects=self.project,
            task_type=self.task_type,
            creator=self.user,
            created_at=timezone.now(),
            description="Test comment",
            assigned_to=self.user,
            status="In progress",
        )
        self.task2 = Task.objects.create(
            title="Test Task2",
            deadline=deadline,
            projects=self.project2,
            task_type=self.task_type,
            creator=self.user,
            created_at=timezone.now(),
            description="Test comment",
            assigned_to=self.user,
            status="In progress",
        )
        self.task3 = Task.objects.create(
            title="Test Task2",
            deadline=deadline,
            projects=self.project2,
            task_type=self.task_type,
            creator=self.user,
            created_at=timezone.now(),
            description="Test comment",
            assigned_to=self.user,
            status="In progress",
        )
        self.url = reverse("projects:task-list")
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/task-list.html")

    def test_my_task_context_correct(self):
        data = {
            "projects": self.project2.pk,
        }
        response = self.client.get(self.url, data)
        self.assertEqual(response.status_code, 200)
        filtered_tasks = response.context["tasks"]
        self.assertEqual(len(filtered_tasks), 2)


class ProjectUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password")
        self.new_user = User.objects.create_user(
            username="testuser2",
            password="password")
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Description")
        self.url = reverse("projects:project_admin",
                           kwargs={"pk": self.project.pk})
        self.client.force_login(self.user)
        self.project.managements.add(self.user)

    def test_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/project-admin.html")

    def test_update_project_members(self):
        data = {
            "projects": self.user.pk,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        updated_project = Project.objects.get(pk=self.project.pk)

        self.assertNotIn(updated_project, self.user.projects.all(),)

    def test_update_project_management(self):
        data = {
            "projects": self.new_user.pk,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)

        updated_project = Project.objects.get(pk=self.project.pk)

        self.assertIn(self.user, updated_project.managements.all())

    def test_send_management_invitation(self):
        data = {
            "member": self.user.pk,
        }

        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)
        updated_project = Project.objects.get(pk=self.project.pk)
        self.assertIn(self.user, updated_project.managements.all())
