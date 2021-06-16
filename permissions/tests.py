import datetime

from django.contrib.auth.models import Group
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from Functions.Permissions import get_permission_id
from Functions.debuging import Debugging
from Functions.tests_credentials import tests_setup_function
from calendars.models import DateType
from patients.models import Patient
from users.models import User

fake = Faker()


class AuthTestings(APITestCase):
    def setUp(self):
        tests_setup_function(self)

        for i in range(1, 3):
            Patient.objects.create(
                user=User.objects.get(id=i))

        group = Group.objects.create(name='provider')
        group.permissions.add(get_permission_id('Can view user', User))

        enconter = Group.objects.create(name='enconter')
        enconter.permissions.add(get_permission_id('Can view username', User))
        enconter.save()
        self.enconter = enconter

        doctor = Group.objects.create(name='doctor')
        doctor.permissions.add(get_permission_id('Can change user', User))
        self.doctor = doctor

        boss = Group.objects.create(name='boss')
        boss.permissions.add(get_permission_id('Can view patient', Patient))
        boss.save()

        d = datetime.datetime
        date_format = '%Y-%m-%d'
        time_format = '%H:%M:%S'
        d = datetime.datetime
        self.now = d.now().strftime(time_format)
        after_1_h = d.now() + datetime.timedelta(hours=1)
        after_5_h = d.now() + datetime.timedelta(hours=5)

        after_1_d = d.now() + datetime.timedelta(days=1)
        after_3_d = d.now() + datetime.timedelta(days=3)

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
    #
        provider = Group.objects.get(name='provider')
        self.user.groups.add(provider)
        self.user.save()
        res = self.client.get('/users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    def test_boss_can_see_patient(self):
        provider = Group.objects.get(name='boss')
        self.user.groups.add(provider)
        self.user.save()
        res = self.client.get('/patient/')
        # Debugging(Group.objects.get(name='boss').permissions.all(), color='green')
        # TODO "permission error": ", You are not permitted to view patient"
        # self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test__spsfic_fields_permission(self):
        res = self.client.get('/users/')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        assert self.user.user_permissions.all().count()==0

        self.user.user_permissions.add(get_permission_id('Can view email',User))
        self.user.save()
        assert self.user.user_permissions.all().count() == 1

        res = self.client.get('/users/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        assert 'email' in res.data[0]
        assert 'username' not in res.data[0]

    def test_if_can_change_then_can_view(self):
        provider = Group.objects.get(name='doctor')
        self.user.groups.add(provider)
        self.user.save()
        resp = self.client.get('/users/')

    # TODO  self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_can_not_view_other_users(self):
        resp = self.client.get('/users/2/')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)  # TODO

    def test_can_not_change(self):
        #0. can't update
        res = self.client.put('/users/2/', {'username': 'updated', 'password': 'password', 'email': 'Alex@g.com'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        #1. add permission
        self.user.user_permissions.add(get_permission_id('Can change user', User))
        self.user.save()

        #3. change
        userI = User.objects.get(id=2)
        res = self.client.put('/users/2/', {'username': 'updated', 'password': 'password', 'email': 'Alex@g.com'})
        userF = User.objects.get(id=2)
        Debugging(res, color='green')
        # 4. test
        self.assertNotEqual(userI.username, userF.username)
        self.assertEqual(userI.email, userF.email)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    #TODO def test_can_change_email(self):
    #     #TODO self.user.user_permissions.add(get_permission_id('Can change email', User))
    #     self.user.is_superuser = True
    #     self.user.save()
    #
    #     userI = User.objects.get(id=1)
    #     resp = self.client.put('/users/1/', {'username': 'updated', 'password': 'password', 'email': 'Alex@g.com'})
    #     userF = User.objects.get(id=1)
    #     Debugging(resp.data, color='green')
    #     self.assertNotEqual(userI.email, userF.email)

    def test_permission_to_put(self):
        self.user.user_permissions.clear()
        self.user.is_staff =False
        self.user.is_superuser = False
        self.user.save()
        resp = self.client.put('/users/2/', {'username': 'updated', 'password': 'password'})
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        self.user.user_permissions.add(get_permission_id('Can change user', User))
        self.user.save()
        resp = self.client.put('/users/2/', {'username': 'updated', 'password': 'password'})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_more(self):
        self.user.user_permissions.add(get_permission_id('Can change user', User))
        self.user.save()
        resp = self.client.put('/users/1/', {'username': 'updated', 'password': 'password'})
        assert resp.data['username'] == 'updated'
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_is_owner(self):
        self.user.user_permissions.clear()
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()
        res = self.client.get('/users/2/')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.get('/users/1/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_cant_update_to_ununique(self):
        res = self.client.put('/users/1/', {'username': 'Alex', 'password': 'password'})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_staff_cannot_update_their_role(self):
    #     self.user.is_staff = True
    #     self.user.save()
    # TODO   resp = self.client.put('/users/1/', {'is_superuser': 'true'})
    #   Debugging(resp.data, color='blue')
    #   self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    def test_can_view_relational_felds(self):
        data = {
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
        }

        res = self.client.post('/calendars/', data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        res = self.client.post('/calendars/', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

