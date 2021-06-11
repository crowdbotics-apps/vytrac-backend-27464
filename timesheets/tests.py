import datetime
import difflib

from rest_framework import status
from rest_framework.test import APITestCase

from Functions.debuging import Debugging
from Functions.tests_credentials import tests_setup_function
from timesheets.models import Column, Value


def prime(num):
    for x in range(2, num):
        if num % x == 0:
            return False
        return True


class TestTimeSheets(APITestCase):
    def setUp(self):
        tests_setup_function(self)

        cal1 = Column.objects.create(name='oxygen', user=self.user)
        cal2 = Column.objects.create(name='prusser', user=self.user)
        cal3 = Column.objects.create(name='late', user=self.user)

        for i in range(4):
            Value.objects.create(column=cal1, field_value=i)

        for i in range(4):
            Value.objects.create(column=cal2, field_value=str(i + 1))

        for i in range(4):
            Value.objects.create(column=cal3, field_value=str(prime(i)))

    def test_statistics_url(self):
        res = self.client.get('/statistics/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_statistics_url_post(self):
        res = self.client.post('/statistics/',
                               {
                                   "field_value": "22",
                                   "name": "ccc",
                                   "action": "added",
                                   "seen_by": [1],
                                   "date_created": "2021-06-09T10:42:41.458057Z",
                                   "column": {
                                       "name": "xx",
                                       "user": 1
                                   }
                               }
                               )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_typost(self):

        data = {
            "field_value": "22",
            "name": "ccc",
            "action": "added",
            "seen_by": [1],
            "date_created": "2021-06-09T10:42:41.458057Z",
            "column": {
                "name": "oxgyn",
                "user": 1
            }
        }
        res = self.client.post('/statistics/', data)

        assert "Did you mean ['oxygen']?" in str(res.data)
        self.assertNotEqual(res.status_code, status.HTTP_201_CREATED)

        data['sure'] = "true"
        res = self.client.post('/statistics/', data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_latest_earliest(self):
        res = self.client.get('/statistics/?latest=true')
        assert res.data[0]['column']['name'] == 'late'

        res = self.client.get('/statistics/?earliest=true')
        assert res.data[0]['column']['name'] == 'oxygen'

    def test_mutli_quries(self):
        res = self.client.get('/statistics/?earliest=true&fields=field_value,date_created')
        assert 'seen_by' not in str(res.data)
        assert 'field_value' in str(res.data)

    def test_depth_qures(self):
        res = self.client.get('/statistics/?column__name=oxygen')
        for i in res.data:
            assert i['column']['name'] == 'oxygen'

        res = self.client.get('/statistics/?column__name=late')
        for i in res.data:
            assert i['column']['name'] == 'late'

    # def test_timesheet_register_patients_data(self):
    #     assert ChangeTrack.objects.all().count() == 3
    #
    #     patient_res = self.client.post('/patient/', {
    #         "prescriptions": "",
    #         "blood_pressure": "120/80",
    #         "created_by": 1,
    #         "care_taker": [1],
    #         "booked_servces": [],
    #         "symptoms": []}, format='json')
    #     self.assertEqual(patient_res.status_code, status.HTTP_201_CREATED)
    #     trackes = ChangeTrack.objects.all().count()
    #     assert trackes > 3
    #     #
    #     patient_res = self.client.put(
    #         '/patient/1/', {'blood_pressure': '130/85'}, format='json')
    #     self.assertEqual(ChangeTrack.objects.all().count(), trackes + 1)
    #
    #     patient_res = self.client.put(
    #         '/patient/1/', {'blood_pressure': '110/80'}, format='json')
    #     assert ChangeTrack.objects.all().count() == trackes + 2
    #
    #     patient_res = self.client.put(
    #         '/patient/1/', {'blood_pressure': '120/80'}, format='json')
    #     assert ChangeTrack.objects.all().count() == trackes + 3
    #
    #     res = self.client.get('/statistics/?resample=day&target=id')
    #
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    #     patient_res = self.client.post('/patient/', {
    #         "prescriptions": "",
    #         "blood_pressure": "999999/0000",
    #         "created_by": 1,
    #         "care_taker": [1],
    #         "booked_servces": [],
    #         "symptoms": []}, format='json')
    #     assert patient_res.data['id'] == 2
    #     self.assertGreaterEqual(
    #         ChangeTrack.objects.all().count(), trackes + 20)
    #     self.assertEqual(patient_res.status_code, status.HTTP_201_CREATED)
    #
    #     res = self.client.get(
    #         '/statistics/'
    #         '?object_id=1'
    #         '&fields=object_id'
    #
    #     )
    #     for i in res.data:
    #         assert i['object_id'] == 1
    #     assert "field_target" not in str(res.data)
    #     assert "object_id" in str(res.data)
    #
    #     res = self.client.get(
    #         '/statistics/'
    #         '?object_id=2'
    #         '&fields=object_id'
    #     )
    #     for i in res.data:
    #         assert i['object_id'] == 2
    #
    # def test_statistics(self):
    #     res = self.client.get('/statistics/?'
    #                           '&cal=max'
    #                           "&resample=2H"
    #                           '&field_target=blood_pressure'
    #                           )
    #
    #     assert len(res.data) == 2
    #     assert '220/80' in str(res.data)
    #     assert '210/80' not in str(res.data)
    #
    #     res = self.client.get('/statistics/?'
    #                           # '?field_value__gt="210/80'
    #                           '&cal=min'
    #                           # "&fields=field_value,field_target,date_created,object_id"
    #                           "&resample=2H"
    #                           '&field_target=blood_pressure'
    #                           )
    #     # Debugging(res.data, color='green')
    #     # TODO
    #     # assert len(res.data) == 2
    #     # assert '220/80' not in str(res.data)
    #     # assert '210/80' in str(res.data)
    #
    #     res = self.client.get('/statistics/?'
    #                           # '?field_value__gt="210/80'
    #                           '&cal=min'
    #                           # "&fields=field_value,field_target,date_created,object_id"
    #                           "&resample=1D"
    #                           '&field_target=blood_pressure'
    #                           )
    #     assert len(res.data) == 1
    #     assert '210/80' in str(res.data)
    #     assert '230/80' not in str(res.data)
    #
    # def test_lookups(self):
    #     res = self.client.get(
    #         '/statistics/?field_value__gt=210/80&fields=field_value')
    #
    #     assert '210/80' not in str(res.data)
    #     assert '220/80' in str(res.data)
    #     #
    #     res = self.client.get(
    #         '/statistics/?field_value__lt=220/80&fields=field_value')
    #     assert '210/80' in str(res.data)
    #     assert '220/80' not in str(res.data)
    #
    # def test_auth(self):
    #     res = self.client.get(
    #         '/statistics/')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #
    #     self.user.is_staff = False
    #     self.user.is_superuser = False
    #     self.user.save()
    #     res = self.client.get(
    #         '/statistics/')
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    # def test_cant_user_cal_and_fields(self):
    #     res = self.client.get(
    #         '/statistics/?fields=field_value&cal=max')
    #
    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #
    #     res = self.client.get(
    #         '/statistics/?fields=field_value')
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)

    # def test_statistics_with_filters(self):
    #     res = self.client.get('/statistics/?'
    #                           '?field_value__gt="210/80'
    #                           '&cal=max'
    #                           "&fields=field_value,field_target,date_created,object_id"
    #                           "&resample=1D"
    #                           '&field_target=blood_pressure'
    #                           )
    #     assert len(res.data) == 1
    #     assert '230/85' in str(res.data)
    #     assert '210/80' not in str(res.data)

    # def test_durations(self):
    #
    #     # TODO test_durations
    #     def prime(num):
    #         for x in range(2, num):
    #             if num % x == 0:
    #                 return False
    #         return True
    #
    #     for i in range(1,10):
    #         new = ChangeTrack.objects.create(field_target='is_seen', field_value=str(prime(i)), object_id='1')
    #         new.date_created = '2021-06-0'+f'{i}'+'T13:48:10.082531Z'
    #         new.save()
    #
    #     res = self.client.get('/statistics/?'
    # '&cal=max'
    # "&fields=field_value,field_target,date_created,object_id"
    # "&resample=1D"
    # '&field_target=blood_pressure'
    # )
    # Debugging(res.data, color='green')

    # assert len(res.data) == 1
    # assert '230/85' in str(res.data)
    # assert '210/80' not in str(res.data)
