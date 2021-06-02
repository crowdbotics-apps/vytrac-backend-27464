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
      # TODO   Debugging(res.data, color='red')

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

    def test_staff_cannot_update_their_role(self):
        self.user.is_staff = True
        self.user.save()
      # TODO   resp = self.client.put('/users/1/', {'is_superuser': 'true'})
      #   Debugging(resp.data, color='blue')
      #   self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
