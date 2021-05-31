from MyFunctions import get_permission_id
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from users.models import User

from rest_framework.test import APIRequestFactory
from tests_credentials import tests_setup_function

# class AuthTestings(APITestCase):
#     def setUp(self):

#         self.register_data = {'email': 'newusername@g.com', 'username': 'newusername',
#                               'password': 'password', 'password2': 'password', }
#         self.login_data = {'username': 'newusername', 'password': 'password'}
#       #TODO login with user2   tests_setup_function(self)

#     def test_permission(self):

#         User.objects.get(username='newusername').user_permissions.add(
#             get_permission_id('Can view phone number'))
#         resp = self.client.get('/users/')
#         # assert len(resp.data[0]) == 1 #TODO

#         user2 = self.user2.user_permissions.add(24)
#         user2.save()

#         resp = self.client.get('/users/')
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)

#         resp = self.client.get('/users/1/')
#         self.assertEqual(resp.status_code, status.HTTP_200_OK)

#         user2.user_permissions.add(24)
#         user2.save()
#         resp = self.client.get('/users/')
#         assert len(resp.data[0]) >= 20
