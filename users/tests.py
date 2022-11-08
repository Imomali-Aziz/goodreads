from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegisterTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("register"),
            data={
                "username": "test_user",
                "first_name": "test",
                "last_name": "user",
                "email": "test@user.com",
                "password": "testpassword"
            }
        )
        user = User.objects.get(username="test_user")

        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "user")
        self.assertEqual(user.email, "test@user.com")
        self.assertNotEqual(user.password, 'testpassword')
        self.assertTrue(user.check_password('testpassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('register'),
            data={
                'first_name': 'test',
                'email': 'test@user.com'
            }
        )

        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse("register"),
            data={
                "username": "test_user",
                "first_name": "test",
                "last_name": "user",
                "email": "invalid_email",
                "password": "testpassword"
            }
        )
        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        user = User.objects.create_user(username='test_user')
        user.set_password('somepassword')
        user.save()

        response = self.client.post(
            reverse("register"),
            data={
                "username": "test_user",
                "password": "testpassword"
            }
        )
        user_count = User.objects.count()

        self.assertEqual(user_count, 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='test_user')
        user.set_password('somepassword')
        user.save()

    def test_user_logged(self):
        self.client.post(
            reverse('login'),
            data={
                'username': 'test_user',
                'password': 'somepassword'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_password(self):
        self.client.post(
            reverse('login'),
            data={
                'username': 'wrong_user',
                'password': 'somepassword'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('login'),
            data={
                'username': 'test_user',
                'password': 'wrong_passsword'
            }
        )
        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_user_logged_out(self):
        self.client.login(username='test_user', password='somepassword')

        self.client.get(reverse('logout'))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.url, reverse('login') + '?next=/users/profile/')

    def test_profile_details(self):
        user = User.objects.create_user(username='test_user', first_name='Test', last_name='User',
                                        email='test@user.com')
        user.set_password('somepassword')
        user.save()

        self.client.login(username='test_user', password='somepassword')

        response = self.client.get(reverse('profile'))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
