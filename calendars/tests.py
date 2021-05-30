import datetime
from re import DEBUG
from calendars import models
from calendars.models import Date, DateType
from django.contrib.auth.models import Group
from django.db.models.query_utils import select_related_descend
from django.urls import reverse
from django.utils.functional import empty
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import RequestsClient
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from users.models import USERNAME, User
from rest_framework.test import force_authenticate
from requests.auth import HTTPBasicAuth

from rest_framework.test import APIRequestFactory
from users.views import UsersView


login_data = {'username': 'newusername',
              'password': 'password'}


class CalinderTests(APITestCase):

    def test_can_not_create_old_date(self):
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
        resp = client.get('/calendars/', format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # TODO create_res = client.post('/calendars/', {
        #     "title": "first",
        #     "description": "",
        #     "start": after_5_h,
        #     "end": after_5_h,
        #     "created_by": 1,
        #     "date_type": 1,
        #     "users": [1]
        # }, format='json')
        # assert 'Start date must be before the end date.' in create_res.data['non_field_errors']
        # self.assertEqual(create_res.status_code, status.HTTP_400_BAD_REQUEST)

        # TODO create_res = client.post('/calendars/', {
        #     "title": "first",
        #     "description": "",
        #     "start": '2021-01-28T10:30:50.884397Z',
        #     "end": '2021-01-28T13:30:50.884397Z',
        #     # "created_by": 1,
        #     "date_type": 1,
        #     "users": [1]
        # }, format='json')
        # assert "You can't have a meeting start or end before now." in str(
        #     create_res.data)
        # self.assertEqual(create_res.status_code, status.HTTP_400_BAD_REQUEST)
        # assert len(Date.objects.all()) == 0

        # TODO create_res = client.post('/calendars/', {
        #     "title": "first",
        #     "description": "",
        #     "start": after_1_h,
        #     "end": after_5_h,
        #     "date_type": 1,
        #     "users": [1]
        # }, format='json')
        # self.assertEqual(create_res.status_code, status.HTTP_201_CREATED)
        # assert len(Date.objects.all()) >= 1
        # new_date = Date.objects.create(title='near', start=after_1_h, end=after_5_h,
        #                                created_by=User.objects.get(id=1))
        # new_date2 = Date.objects.create(title='far', start=after_10_h, end=after_11_h,
        #                                 created_by=User.objects.get(id=1))
        # new_date0 = Date.objects.create(title='old', start='2021-01-28T10:30:50.884397Z', end='2021-01-28T13:30:50.884397Z',
        #                                 created_by=User.objects.get(id=1))
        # new_date.users.set([user, user2])
        # assert len(Date.objects.all()) == 4
        # assert len(Date.objects.filter(users__in=[user, user2])) == 3

        # dates = Date.objects.all()

        # assert len(dates) == 4
        # dates = dates.filter(start__gte=now, end__gte=now)
        # assert len(dates) == 3

        # TODO create_res = client.post('/calendars/', {
        #     "title": "this is ntersected",
        #     "description": "",
        #     "start": after_2_h,
        #     "end": after_3_h,
        #     "date_type": 1,
        #     "users": [1]
        # }, format='json')
        # assert 'overlap error' in str(create_res.data)
        # self.assertEqual(create_res.status_code, status.HTTP_400_BAD_REQUEST)
