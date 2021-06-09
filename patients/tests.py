import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from Functions.debuging import Debugging
from Functions.tests_credentials import tests_setup_function
from calendars.models import DateType
from users.models import Availablity


class PatientsAppTests(APITestCase):
    def setUp(self):
        tests_setup_function(self)

    def test_emergency_contct_link(self):
        res = self.client.get('/patient/emergency_contact/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # res = self.client.get('/patient/emergency_contact/1/', )
        # self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_patient_relational_data(self):
        res = self.client.post('/patient/',
                               {
                                   "created_by": 1,
                                   "user": 2,
                               }
                               )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #
        res = self.client.post('/patient/emergency_contact/',
                               {
                                   "patient": [1],
                                   "first_name": "Sam",
                                   "relationship": 'siblings',

                               }
                               )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        #
        res = self.client.get('/patient/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        emergency_contact = res.data[0]['emergency_contact'][0]
        assert len(emergency_contact) > 1
        assert 'patient' not in str(emergency_contact)

    # def test_create_stymptoms_from_patient_profile(self):
    #     res = self.client.post('/patient/', {
    #         "prescriptions": "",
    #         "blood_pressure": "120/80",
    #         "created_by": 1,
    #         "care_taker": [1],
    #         "booked_servces": [],
    #        })
    #     assert len(res.data['symptoms']) == 2
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
