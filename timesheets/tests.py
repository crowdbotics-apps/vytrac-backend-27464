import datetime

from rest_framework import status
from rest_framework.test import APITestCase

from Functions.debuging import Debugging
from Functions.tests_credentials import tests_setup_function
from timesheets.models import ChangeTrack


class TestTimeSheets(APITestCase):
    def setUp(self):
        assert ChangeTrack.objects.all().count() == 0
        d = datetime.datetime
        object1 = ChangeTrack.objects.create(
            field_target='blood_pressure', field_value='220/80')
        object2 = ChangeTrack.objects.create(
            field_target='blood_pressure', field_value='210/80')
        object3 = ChangeTrack.objects.create(
            field_target='blood_pressure', field_value='230/85')
        time = d.now() + datetime.timedelta(hours=1)
        object1.date_created = time
        object1.save()

        time = d.now() + datetime.timedelta(hours=2)
        object2.date_created = time
        object2.save()

        time = d.now() + datetime.timedelta(hours=3)
        object3.date_created = time
        object3.save()

        tests_setup_function(self)

    def test_(self):
        res = self.client.get(
            '/statistics/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_timesheet_register_patients_data(self):
        assert ChangeTrack.objects.all().count() == 3

        patient_res = self.client.post('/patient/', {
            "prescriptions": "",
            "blood_pressure": "120/80",
            "created_by": 1,
            "care_taker": [1],
            "booked_servces": [],
            "symptoms": []}, format='json')
        self.assertEqual(patient_res.status_code, status.HTTP_201_CREATED)
        trackes = ChangeTrack.objects.all().count()
        assert trackes > 3
    #
        patient_res = self.client.put(
            '/patient/1/', {'blood_pressure': '130/85'}, format='json')
        self.assertEqual(ChangeTrack.objects.all().count(), trackes + 1)

        patient_res = self.client.put(
            '/patient/1/', {'blood_pressure': '110/80'}, format='json')
        assert ChangeTrack.objects.all().count() == trackes + 2

        patient_res = self.client.put(
            '/patient/1/', {'blood_pressure': '120/80'}, format='json')
        assert ChangeTrack.objects.all().count() == trackes + 3

        res = self.client.get('/statistics/?resample=day&target=id')

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        patient_res = self.client.post('/patient/', {
            "prescriptions": "",
            "blood_pressure": "999999/0000",
            "created_by": 1,
            "care_taker": [1],
            "booked_servces": [],
            "symptoms": []}, format='json')
        assert patient_res.data['id'] == 2
        self.assertGreaterEqual(
            ChangeTrack.objects.all().count(), trackes + 20)
        self.assertEqual(patient_res.status_code, status.HTTP_201_CREATED)

        res = self.client.get(
            '/statistics/?fields=field_target,object_id')
        assert 'object_id' in str(res.data)

        res = self.client.get(
            '/statistics/?object_id=1&fields=object_id')
        # assert "'object_id', 2" in str(res.data)
        # assert "field_target" not in str(res.data)
        #
        # res = self.client.get(
        #     '/statistics/?object_id=2&fields=object_id')
        # assert "'object_id', 2" in str(res.data)
        # assert "OrderedDict" in str(res.data)

    def test_statistics(self):
        url = '?field_value__gt=210/80'
        # url += '&target=field_value'
        # url += '&field_target=blood_pressure'
        # cal = '&cal=min&resample=1D'
        # url += '&target=field_value'
        # url += '&field_target=blood_pressure'
        res = self.client.get('/statistics/'+url)

        assert '210/80' not in str(res.data)
        assert '220/80' in str(res.data)
        #
        res = self.client.get('/statistics/?field_value__gt="210/80&cal=max&resample=1D&target=field_value&field_target=blood_pressure')
        Debugging(res.data)
        # assert '210/80' not in str(res.data)
        # assert '230/85' in str(res.data)

    # def test_lookups(self):
    #     res = self.client.get(
    #         '/statistics/?field_value__gt=210/80&fields=field_value')
    #     Debugging(res.data, color='red')
    #     assert '210/80' not in str(res.data)
    #     assert '220/80' in str(res.data)
    #
    #     res = self.client.get(
    #         '/statistics/?field_value__lt=220/80&fields=field_value')
    #     assert '210/80' in str(res.data)
    # assert '220/80' not in str(res.data)

    def test_auth(self):
        res = self.client.get(
            '/statistics/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()
        res = self.client.get(
            '/statistics/')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_user_cal_and_fields(self):
        res = self.client.get(
            '/statistics/?fields=field_value&cal=max')
        Debugging(res.data, color='blue')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.get(
            '/statistics/?fields=field_value')
        Debugging(res.data, color='blue')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
