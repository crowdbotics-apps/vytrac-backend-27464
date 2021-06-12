import datetime
from safedelete.queryset import SafeDeleteQueryset
from safedelete.models import SafeDeleteModel


from safedelete import models as SM
from rest_framework import status
from rest_framework.test import APITestCase

from Functions.debuging import Debugging
from Functions.tests_credentials import tests_setup_function
from calendars.models import DateType
from users.models import Availablity, User

login_data = {'username': 'Clover',
              'password': 'password'}


class CalinderTests(APITestCase):
    def setUp(self):
        tests_setup_function(self)

    def test_can_not_create_old_date(self):
        pass
        # res = self.client.get('/users/', format='json')
        # Debugging(User.objects.all(), color='green')
        # User.objects.get(id=3).delete()
        # Debugging(User.objects.all(), color='blue')
        # Debugging(User.objects.all(), color='blue')
        # self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Debugging(res.data, color='green')

