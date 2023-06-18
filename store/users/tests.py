from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {'first_name': 'Sasha', 'last_name': 'Loc', 'username': 'SashaLCow',
                     'email': 'alexnaderlco34232@gmail.com', 'password1': 'AzZa1234zxcv',
                     'password2': 'AzZa1234zxcv'}

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post(self):
        response = self.client.post(self.path, self.data)
        username = self.data['username']

        # check creating user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # create emailver
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertEqual(email_verification.first().expiration.date(),
                         (now() + timedelta(hours=48)).date()
                         )

        def test_user_registration_post_error(self):
            User.objects.create(username=self.data['username'])
            response = self.client.post(self.path, self.data)

            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
