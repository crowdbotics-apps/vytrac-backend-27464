from tests_credentials import tests_setup_function
from MyFunctions import get_permission_id
from notifications.consumers import Alerts
from channels.testing import HttpCommunicator
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


class MyTests(TestCase):
    def setUp(self):
        tests_setup_function(self)

    async def test_my_consumer(self):
        communicator = HttpCommunicator(
            Alerts, "GET", f"/alerts/?token={self.token}/")
        # response = await communicator.get_response()
        # print('======================')
        # print(response)
        # print('======================')
# response["headers"]
# self.assertEqual(response["body"], b"test response")
# self.assertEqual(response["status"], 200)


class AlertsTests(APITestCase):
    def setUp(self):
        date_format = '%Y-%m-%d'
        time_format = '%H:%M:%S'
        d = datetime.datetime
        self.now = d.now().strftime(time_format)
        after_1_h = d.now()+datetime.timedelta(hours=1)
        after_5_h = d.now()+datetime.timedelta(hours=5)
        self.after_1_h = after_1_h.strftime(time_format)
        self.after_5_h = after_5_h.strftime(time_format)

        after_2_h = d.now()+datetime.timedelta(hours=2)
        after_3_h = d.now()+datetime.timedelta(hours=3)
        self.after_2_h = after_2_h.strftime(time_format)
        self.after_3_h = after_3_h.strftime(time_format)

        after_10_h = d.now()+datetime.timedelta(hours=10)
        after_11_h = d.now()+datetime.timedelta(hours=11)
        self.after_10_h = after_10_h.strftime(time_format)
        self.after_11_h = after_11_h.strftime(time_format)

        after_1_d = d.now()+datetime.timedelta(days=1)
        after_3_d = d.now()+datetime.timedelta(days=3)

        self.after_1_d = after_1_d.strftime(date_format)
        self.after_3_d = after_3_d.strftime(date_format)

        DateType.objects.create(name='meeting')
        DateType.objects.create(name='appointment')
        tests_setup_function(self)

    def test_dates_notifcations(self):
        # TODO Create genral function to reuse in all tests

        DateType.objects.create(name='meeting')
        DateType.objects.create(name='appointment')

        self.assertEqual(Notifications.objects.all().count(), 0)
        res = self.client.post('/calendars/', {
            "title": "first",
            "description": "",
            "start": self.after_1_d,
            "end": self.after_3_d,
            "from_time": self.after_1_h,
            "to_time": self.after_5_h,
            "created_by": 1,
            "date_type": 1,
            "users": [1],
            "recurrence": [
            ],
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Notifications.objects.all().count(), 1)

        # TODO test target`
        # TODO test filter`ing
