
from users.models import User
from rest_framework.test import APIClient

from rest_framework import status


def tests_setup_function(self):

    user2 = User.objects.create(date_joined='2021-05-28T13:30:50.884397Z', username='newusername2', email='newusername2@g.com',
                                password='password', is_email_verified=True, is_role_verified=True, is_staff=True, is_superuser=True)

    user3 = User.objects.create(username='newusername3', email='newusername3@g.com',
                                password='password', is_email_verified=True, is_role_verified=True)
    if (not User.objects.filter(username='newusername').exists()):
        user = User.objects.create(username='newusername', email='newusername@g.com',
                                   password='password', is_email_verified=True, is_role_verified=True, is_staff=True)
    else:
        user = User.objects.get(username='newusername')
    client = APIClient()
    lg_res = client.post('/users/login/',  {'username': 'newusername',
                                            'password': 'password'}, format='json')
    self.user = user
    self.user2 = user2
    self.user3 = user3
    self.token = lg_res.data["access"]
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {self.token}')
    res = client.get('/statistics/?resample=day&target=id')
    self.client = client
    self.assertEqual(res.status_code, status.HTTP_200_OK)
