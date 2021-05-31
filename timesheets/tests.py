from tests_credentials import tests_setup_function
from timesheets.models import ChangeTrack
from manage_patients.models import Profile
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework.test import RequestsClient
from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from users.models import User
from rest_framework.test import force_authenticate
from requests.auth import HTTPBasicAuth

from rest_framework.test import APIRequestFactory
perm_tuple = [(x.id, x.name)
              for x in Permission.objects.all()]

# Create your tests here.


class TestTimeSheets(APITestCase):
    def setUp(self):
        tests_setup_function(self)

    def test_timesheet_register_patients_data(self):
        assert ChangeTrack.objects.all().count() == 0
        patient_res = self.client.post('/patient/', {
            "prescriptions": "",
            "blood_pressure": "120/80",
            "created_by": 1,
            "care_taker": [1],
            "booked_servces": [],
            "symptoms": []}, format='json'
        )
        trackes = ChangeTrack.objects.all().count()
        assert trackes > 0
        patient_res = self.client.put(
            '/patient/1/',  {'blood_pressure': '130/85'}, format='json')
        self.assertEqual(ChangeTrack.objects.all().count(), trackes+1)

        patient_res = self.client.put(
            '/patient/1/',  {'blood_pressure': '110/80'}, format='json')
        assert ChangeTrack.objects.all().count() == trackes+2

        patient_res = self.client.put(
            '/patient/1/',  {'blood_pressure': '120/80'}, format='json')
        assert ChangeTrack.objects.all().count() == trackes+3

        res = self.client.get('/statistics/?time_frame=day&target=id')
        # print('======================')
        # TODO print(res.data)
        # print('======================')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patient_res = self.client.post('/patient/', {
            "prescriptions": "",
            "blood_pressure": "999999/0000",
            "created_by": 1,
            "care_taker": [1],
            "booked_servces": [],
            "symptoms": []}, format='json')
        assert patient_res.data['id'] == 2
        self.assertEqual(ChangeTrack.objects.all().count(), trackes+3+10)
        self.assertEqual(patient_res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(
            '/statistics/?field_target=blood_pressure&object_id=1&time_frame=minute&target=field_value&cal=max')
        assert '130' in str(res.data)
        assert not '999999' in str(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(
            '/statistics/?field_target=blood_pressure&object_id=2&time_frame=minute&target=field_value&cal=max')
        assert not '130' in str(res.data)
        assert '999999' in str(res.data)
        # print('======================')
        # print(res.data)
        # print('======================')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.get(
            '/statistics/?id__lt=3&fields=id')
        print('res test debug======================')
        # # TODO why this return all data?
        # Note it in urls.py:68 it return the correct data.
        # print(res.data)
        # print('======================')
        # assert '999999' in str(res.data)
        # self.assertEqual(res.status_code, status.HTTP_200_OK)
