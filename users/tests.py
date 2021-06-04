from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from Functions.MyFunctions import get_permission_id
from Functions.debuging import Debugging
from users.models import User


class AuthTestings(APITestCase):
    def setUp(self):
        self.register_data = {'email': 'newusername@g.com', 'username': 'newusername',
                              'password': 'password', 'password2': 'password', }
        self.login_data = {'username': 'newusername',
                           'password': 'password'}

    register_url = reverse('register')
    login_url = reverse('login')
    logout_url = reverse('logout')
    token_refresh_url = reverse('token_refresh')
    verfy_token_url = reverse('verfy_token')
    reset_email_url = reverse('request-reset-email')
    email_verify_url = reverse('email-verify')
    all_users_url = reverse('all_users')
    user_url = '/users/verify_email/1'

    def test_register(self):
        response = self.client.post(
            self.register_url, self.register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(id=1).username, 'newusername')

    def test_api_jwt_and_permissions_and_users(self):
        assert User.objects.count() == 0
        self.client.post(self.register_url, self.register_data, format='json')
        assert User.objects.count() == 1
        u = User.objects.get(id=1)
        # u.is_active = False
        # u.save()

        resp = self.client.post(
            self.login_url, self.login_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        u.is_active = True
        u.is_email_verified = True
        u.is_role_verified = True
        u.save()

        client = APIClient()
        resp = client.post(
            self.login_url, self.login_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in resp.data)
        token = resp.data['access']
        refresh_token = resp.data['refresh']

        verification_url = '/users/token/verify/'
        resp = self.client.post(
            verification_url, {'token': token}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.client.post(
            verification_url, {'token': 'abc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer abc')
        resp = client.get('/users/', data={'format': 'json'})
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = client.get('/users/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['permission error'],
                         ', You are not permitted to view user')
        u.is_superuser = False
        u.is_staff = False
        u.save()

        resp = client.get('/users/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = client.get('/users/1')
        assert u.id == 1
        # self.assertEqual(resp.status_code, status.HTTP_200_OK) # TODO

        u.user_permissions.add(
            get_permission_id('Can view username'))
        u.save()

        resp = client.get('/users/')
        # assert len(resp.data[0]) == 1
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        u.user_permissions.add(
            get_permission_id('Can view last name'))
        u.save()

        resp = client.get('/users/')
        # assert len(resp.data[0]) == 2
        Debugging(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        u.user_permissions.add(
            get_permission_id('Can view user'))
        u.save()
        resp = client.get('/users/')
        assert len(resp.data[0]) >= 20
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = client.get('/users/1/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        u.user_permissions.add(24)
        u.save()
        resp = client.get('/users/')
        assert len(resp.data[0]) >= 20

        # res = client.get('/users/?fields=is_role_verified,date_joined')
