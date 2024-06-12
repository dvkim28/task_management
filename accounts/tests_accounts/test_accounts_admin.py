from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from projects.models import Project


class AccountsAdminTestCase(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='<EMAIL>',
            password='adminpassword'
        )
        self.project = Project.objects.create(
            name="Test Project",
            description="Test Project",
        )
        self.user = User.objects.create_user(
            username='user',
            email='<EMAIL>',
            password='<PASSWORD>',
            position='SM',
            company='Test Company',
            about_info='Test About Info',
        )
        self.user.projects.add(self.project)

    def test_user_change_list_has_custom_fields(self):
        self.client.login(username='admin', password='adminpassword')
        url = reverse('admin:accounts_user_change', args=[self.user.id])
        response = self.client.get(url)
        self.assertContains(response, self.user.company)
        self.assertContains(response, self.user.position)
        self.assertContains(response, self.user.about_info)
