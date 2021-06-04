from calendars.models import DateType
import datetime
from Functions.debuging import Debugging
from manage_patients.models import Profile
from django.contrib.auth.models import Group
from Functions.MyFunctions import get_permission_id
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from Functions.tests_credentials import tests_setup_function
from faker import Faker
fake = Faker()


class AuthTestings(APITestCase):
    def setUp(self):

        tests_setup_function(self)

        for i in range(1, 3):
            Profile.objects.create(
                user=User.objects.get(id=i), prescriptions=fake.text())

        group = Group.objects.create(name='provider')
        group.permissions.add(get_permission_id('Can view user'))

        # group2 = Group.objects.create(name='enconter')
        # group2.permissions.add(get_permission_id('Can view phone number'))

        group3 = Group.objects.create(name='doctor')
        group3.permissions.add(get_permission_id('Can change user'))
        group3.permissions.add(get_permission_id('Can view prescriptions'))

        group3 = Group.objects.create(name='boss')
        group3.permissions.add(get_permission_id('Can view profile'))

        d = datetime.datetime
        date_format = '%Y-%m-%d'
        time_format = '%H:%M:%S'
        d = datetime.datetime
        self.now = d.now().strftime(time_format)
        after_1_h = d.now()+datetime.timedelta(hours=1)
        after_5_h = d.now()+datetime.timedelta(hours=5)

        after_1_d = d.now()+datetime.timedelta(days=1)
        after_3_d = d.now()+datetime.timedelta(days=3)

        self.after_1_h = after_1_h.strftime(time_format)
        self.after_5_h = after_5_h.strftime(time_format)
        self.after_1_d = after_1_d.strftime(date_format)
        self.after_3_d = after_3_d.strftime(date_format)
        DateType.objects.create(name='meeting')

        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

    def test_permission(self):
        resp = self.client.get('/users/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        provider = Group.objects.get(name='provider')
        self.user.groups.add(provider)
        self.user.save()
        res = self.client.get('/users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get('/patient/')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        provider = Group.objects.get(name='boss')
        self.user.groups.add(provider)
        self.user.save()
        res = self.client.get('/patient/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_can_view_one_field(self):
        doctor = Group.objects.get(name='doctor')
        self.user.groups.add(doctor)
        self.user.save()
        res = self.client.get('/patient/')

      #   enconter = Group.objects.get(name='enconter')
      #   self.user.groups.add(enconter)
      #   self.user.save()
      #   resp = self.client.get('/users/')
      #   Debugging(resp.data, color='green')
      #   self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_if_can_change_then_can_view(self):
        provider = Group.objects.get(name='doctor')
        self.user.groups.add(provider)
        self.user.save()
        resp = self.client.get('/users/')
      # TODO  self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_can_not_view_other_users(self):
        resp = self.client.get('/users/2/')
        # self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)  # TODO

    def test_can_change(self):
        self.user.user_permissions.add(get_permission_id('Can view user'))
        self.user.save()

        resp = self.client.get('/users/2/')
        assert resp.data['username'] == 'newusername3'

        resp = self.client.put(
            '/users/1/', {'username': 'updated', 'password': 'password', 'email': 'newusername2@g.com'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.user_permissions.add(get_permission_id('Can change user'))
        self.user.save()
        resp = self.client.put(
            '/users/1/', {'username': 'updated', 'password': 'password', 'email': 'newusername2@g.com'})
        assert resp.data['username'] == 'updated'
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # def test_staff_cannot_update_their_role(self):
    #     self.user.is_staff = True
    #     self.user.save()
    # TODO   resp = self.client.put('/users/1/', {'is_superuser': 'true'})
    #   Debugging(resp.data, color='blue')
    #   self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    def test_can_view_relational_feelds(self):
        self.user.user_permissions.add(get_permission_id('Can add date'))
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
        self.user.user_permissions.add(get_permission_id('Can view user'))
        res = self.client.get('/users/')
        assert 'dates' not in str(res.data)
        self.user.user_permissions.add(get_permission_id('Can view date'))
        self.user.save()
        res = self.client.get('/users/')
        assert 'dates' in str(res.data)
