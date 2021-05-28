from timesheets.models import ChangeTrack
from patientsprofiles.models import PatientProfile
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
from users.views import UsersView
perm_tuple = [(x.id, x.name)
              for x in Permission.objects.all()]

# Create your tests here.


class TestTimeSheets(APITestCase):
    

    
    def test_statstics(self):
        user1 = User.objects.create(date_joined='2021-05-28T13:30:50.884397Z',username='newusername2', email='newusername2@g.com', password='password', is_email_verified=True, is_role_verified=True, is_staff=True, is_superuser=True)
        user3 = User.objects.create(username='newusername3', email='newusername3@g.com', password='password', is_email_verified=True, is_role_verified=True, is_staff=True)
        if (not User.objects.filter(username='newusername').exists()):
            user = User.objects.create(username='newusername', email='newusername@g.com', password='password', is_email_verified=True, is_role_verified=True, is_staff=True)
        else:
            user = User.objects.get(username='newusername')
        client = APIClient()
        lg_res = client.post('/users/login/',  {'username': 'newusername',
                                'password': 'password'}, format='json')
        assert ChangeTrack.objects.all().count() ==0

        newpatient = PatientProfile.objects.create(user=user,blood_pressure='120/80')
        trackes = ChangeTrack.objects.all().count()
        assert trackes >0

        client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {lg_res.data["access"]}')
        res = client.get('/statistics/?time_frame=day&target=id')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patient_res = client .put('/patient/1/',  {'blood_pressure': '130/85'}, format='json')
        assert ChangeTrack.objects.all().count() ==trackes+1
        
        patient_res = client .put('/patient/1/',  {'blood_pressure': '110/80'}, format='json')
        assert ChangeTrack.objects.all().count() ==trackes+2

        patient_res = client .put('/patient/1/',  {'blood_pressure': '120/80'}, format='json')
        assert ChangeTrack.objects.all().count() ==trackes+3

        res = client.get('/statistics/?time_frame=day&target=id')
        # print('======================')
        # TODO print(res.data)
        # print('======================')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patient_res = client.post('/patient/', {
            "prescriptions": "",
            "blood_pressure": "999999/0000",
            "created_by": 1,
            "care_taker": [1],
            "booked_servces": [],
            "symptoms": []}, format='json')
        assert patient_res.data['id']==2
        assert ChangeTrack.objects.all().count() ==trackes+3+9
        self.assertEqual(patient_res.status_code, status.HTTP_201_CREATED)


        res = client.get('/statistics/?field_target=blood_pressure&object_id=1&time_frame=minute&target=field_value&cal=max')
        assert '130'in str(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = client.get('/statistics/?field_target=blood_pressure&object_id=2&time_frame=minute&target=field_value&cal=max')
        assert '999999'in str(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        pass
