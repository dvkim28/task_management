from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse


class UserRegistrationViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="<EMAIL>",
            password="PASSWORD",
            username="testuser",
        )
        self.url = reverse("accounts:user-registration")
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_user_registration_success(self):
        data = {
            "username": "test_user",
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)

        user = get_user_model().objects.get(username="test_user")

        self.assertIsNotNone(user)
        self.assertTrue(check_password("password123", user.password))
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    #
    def test_user_registration_invalid_data(self):
        data = {
            "username": "",
            "email": "invalid-email",
            "password": "123"
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response,
                             "form",
                             "username",
                             "This field is required.")
        self.assertFormError(response,
                             "form",
                             "email",
                             "Enter a valid email address.")

    def test_user_login(self):
        login_success = self.client.login(
            username="testuser",
            password="PASSWORD")
        self.assertTrue(login_success)

        self.assertEqual(int(
            self.client.session["_auth_user_id"]), self.user.pk)


class UserUpdateProfileViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test2@mail.com",
            password="<PASSWORD>",
            username="testuser",
        )
        self.url = reverse("accounts:user-profile-view", args=[self.user.pk])
        self.client.force_login(self.user)
        self.response = self.client.get(self.url)

    def test_user_profile_has_needed_fields(self):
        data = {
            "email": "test@mail.com",
            "first_name": "Test_name",
            "last_name": "test_last_name",
            "position": "Designer",
            "company": "Test_company",
            "about_info": "Test_about",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data["email"])
        self.assertEqual(self.user.first_name, data["first_name"])
        self.assertEqual(self.user.last_name, data["last_name"])
        self.assertEqual(self.user.position, data["position"])
        self.assertEqual(self.user.company, data["company"])
        self.assertEqual(self.user.about_info, data["about_info"])
