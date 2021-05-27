from notifications.models import Notifications
from django.test import TestCase

import datetime
from calendars.models import Date, DateType
from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import include, path, reverse
from rest_framework.test import APITestCase
from users.models import User

from rest_framework.test import APIRequestFactory

perm_tuple = [(x.id, x.name)
              for x in Permission.objects.all()]


login_data = {'username': 'newusername',
              'password': 'password'}

from django.test import TestCase
from channels.testing import HttpCommunicator
from notifications.consumers import WSConsumer





class NotifcationsTests(APITestCase):

    def test_dates_notifcations(self):
        my_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        d = datetime.datetime
        now = d.now().strftime(my_format)
        after_1_h = d.now()+datetime.timedelta(hours=1)
        after_5_h = d.now()+datetime.timedelta(hours=5)
        after_1_h = after_1_h.strftime(my_format)
        after_5_h = after_5_h.strftime(my_format)

        after_2_h = d.now()+datetime.timedelta(hours=2)
        after_3_h = d.now()+datetime.timedelta(hours=3)
        after_2_h = after_2_h.strftime(my_format)
        after_3_h = after_3_h.strftime(my_format)

        after_10_h = d.now()+datetime.timedelta(hours=10)
        after_11_h = d.now()+datetime.timedelta(hours=11)
        after_10_h = after_10_h.strftime(my_format)
        after_11_h = after_11_h.strftime(my_format)

        DateType.objects.create(name='meeting')
        DateType.objects.create(name='appointment')
        user = User.objects.create(
            username='newusername', email='newusername@g.com', password='password', is_email_verified=True, is_role_verified=True, is_staff=True, is_superuser=True)
        user2 = User.objects.create(
            username='other', email='other@g.com', password='password', is_email_verified=True, is_role_verified=True, is_staff=True, is_superuser=True)
        user.user_permissions.add(55)
        user.save()
        client = APIClient()
        lg_res = client.post('/users/login/', login_data, format='json')
        client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {lg_res.data["access"]}')
        assert len(Notifications.objects.all()) == 0
        create_res = client.post('/calendars/', {
            "title": "first",
            "description": "",
            "start": after_1_h,
            "end": after_5_h,
            "date_type": 1,
            "users": [1]
        }, format='json')
        self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        assert len(Notifications.objects.all()) == 1
        # TODO test target
        # TODO test filtering
