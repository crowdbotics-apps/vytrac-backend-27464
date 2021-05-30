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


login_data = {'username': 'newusername',
              'password': 'password'}


def credentialize_tests():
    user = User.objects.create(
        username='newusername', email='newusername@g.com', password='password', is_email_verified=True, is_role_verified=True, is_staff=True, is_superuser=True)
    client = APIClient()
    lg_res = client.post('/users/login/', {'username': 'newusername',
                                           'password': 'password'}, format='json')
    assert lg_res.status_code == status.HTTP_200_OK
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {lg_res.data["access"]}')
    return user, client


# class MyTests(TestCase):
#     client = APIClient()
#     lg_res = client.post('/users/login/', login_data, format='json')
#     token = lg_res.data["access"]

#     async def test_my_consumer(self):
#         pass
#         communicator = HttpCommunicator(
#             Alerts, "GET", f"/alerts/?token={self.token}/")
    # TODO response = await communicator.get_response()
    # response["headers"]
    # self.assertEqual(response["body"], b"test response")
    # self.assertEqual(response["status"], 200)


class AlertsTests(APITestCase):
    my_format = '%Y-%m-%d'
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
    myx = ''

    def test_dates_notifcations(self):
        # TODO Create genral function to reuse in all tests

        DateType.objects.create(name='meeting')
        DateType.objects.create(name='appointment')
        user, client = credentialize_tests()
        user2 = User.objects.create(
            username='other', email='other@g.com', password='password', is_email_verified=True, is_role_verified=True, is_staff=True, is_superuser=True)
        user.user_permissions.add(get_permission_id('Can view user'))
        user.save()

        assert len(Notifications.objects.all()) == 0

        self.assertEqual(Notifications.objects.all().count(), 0)
        # TODO create_res = client.post('/calendars/', {
        #     "id": 3,
        #     "recurrence": [
        #         "1 thursday",
        #         "1 tuesday",
        #         "1 monday",
        #         "1 wednesday"
        #     ],
        #     "date_created": "2021-05-30 12:48:11.816480+00:00",
        #     "title": "",
        #     "description": "",
        #     "start": "2021-05-31",
        #     "end": "2021-06-02",
        #     "from_time": "15:19:00",
        #     "to_time": "18:20:00",
        #     "priority": "low",
        #     "date_type": 1,
        #     "created_by": 1,
        #     "users": [
        #         1
        #     ]
        # }, format='json')
        # print('======================')
        # print(create_res.data)
        # print('======================')

        # self.assertEqual(Notifications.objects.all().count(), 1)

        # TODO test target`
        # TODO test filter`ing
