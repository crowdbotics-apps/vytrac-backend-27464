from rest_framework import status
from rest_framework.test import APIClient

from Functions.debuging import Debugging
from users.models import User

from colorama import Fore, Back


def tests_setup_function(self):
    user, create = User.objects.get_or_create(username='Clover', email='Clover@g.com', password='password')
    user.is_email_verified = True
    user.is_role_verified = True
    user.is_staff = True
    user.is_superuser = True
    user.save()

    user2, create2 = User.objects.get_or_create(date_joined='2021-05-28T13:30:50.884397Z', username='Alex',
                                                email='Alex@g.com', password='password')
    user2.is_email_verified = True
    user2.is_staff = True
    user2.save()
    assert user2.is_superuser == False
    user.save()

    user3, create3 = User.objects.get_or_create(username='Sam', email='Sam@g.com', password='password',
                                                is_email_verified=True)
    user3.is_email_verified = True
    user3.save()

    assert user3.is_staff == False
    assert user3.is_superuser == False

    for i in [create, create2, create3]:
        print(Back.RED + '=========== laready exist =========== ') if not i else None

    client = APIClient()
    lg_res = client.post('/users/login/', {'username': 'Clover', 'password': 'password'})
    lg_res2 = client.post('/users/login/', {'username': 'Alex', 'password': 'password'})
    lg_res3 = client.post('/users/login/', {'username': 'Sam', 'password': 'password'})
    #
    self.user = user
    self.user2 = user2
    self.user3 = user3

    self.token = lg_res.data["access"]
    self.token2 = lg_res2.data["access"]
    self.token3 = lg_res3.data["access"]

    res = client.get('/statistics/')
    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    client = client

    res = client.get('/statistics/')
    self.assertEqual(res.status_code, status.HTTP_200_OK)

    self.client = client
