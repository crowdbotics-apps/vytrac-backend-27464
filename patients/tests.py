import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from Functions.debuging import Debugging
from Functions.tests_credentials import tests_setup_function
from calendars.models import DateType
from users.models import Availablity


class PatientsAppTests(APITestCase):
    def setUp(self):
        # date_format = '%Y-%m-%d'
        # time_format = '%H:%M:%S'
        # d = datetime.datetime
        # self.now = d.now().strftime(time_format)
        # after_1_h = d.now() + datetime.timedelta(hours=1)
        # after_5_h = d.now() + datetime.timedelta(hours=5)
        # self.after_1_h = after_1_h.strftime(time_format)
        # self.after_5_h = after_5_h.strftime(time_format)
        #
        # after_2_h = d.now() + datetime.timedelta(hours=2)
        # after_3_h = d.now() + datetime.timedelta(hours=3)
        # self.after_2_h = after_2_h.strftime(time_format)
        # self.after_3_h = after_3_h.strftime(time_format)
        #
        # after_10_h = d.now() + datetime.timedelta(hours=10)
        # after_11_h = d.now() + datetime.timedelta(hours=11)
        # self.after_10_h = after_10_h.strftime(time_format)
        # self.after_11_h = after_11_h.strftime(time_format)
        #
        # after_1_d = d.now() + datetime.timedelta(days=1)
        # after_3_d = d.now() + datetime.timedelta(days=3)
        #
        # self.after_1_d = after_1_d.strftime(date_format)
        # self.after_3_d = after_3_d.strftime(date_format)
        #
        # DateType.objects.create(name='meeting')
        # DateType.objects.create(name='appointment')
        tests_setup_function(self)
        # availablity = Availablity.objects.create(title='office hourse', created_by=self.user2,
        #                                          start='2022-06-07T08:03:33', end='2023-06-07T08:03:33',
        #                                          recurrence=['1 sunday', '1 monday', '1 tuesday'])
        # self.user2.date_avalable.add(availablity)

    def test_emergency_contct_link(self):
        res = self.client.get('/patient/emergency_contact/', )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # res = self.client.get('/patient/emergency_contact/1/', )
        # self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_goals_link(self):
        res = self.client.get('/patient/goals/', )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_stymptoms_from_patient_profile(self):
        res = self.client.post('/patient/', {
            "prescriptions": "",
            "blood_pressure": "120/80",
            "created_by": 1,
            "care_taker": [1],
            "booked_servces": [],
            "symptoms": [
                {"name": 'Eczema'},
                {"name": 'other'},
            ]})
        assert len(res.data['symptoms']) == 2
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
