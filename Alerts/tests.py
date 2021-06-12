import datetime
import json

import websockets
from channels.testing import WebsocketCommunicator
from rest_framework import status
from rest_framework.test import APITestCase
from asgiref.sync import sync_to_async

from Alerts.consumers import Alerts
from Functions.debuging import Debugging
from Functions.tests_credentials import tests_setup_function
from calendars.models import DateType, Event
from users.models import User


class WebsocketTests(APITestCase):
    def setUp(self):
        tests_setup_function(self)

        self.url = f"alerts/?token={self.token}"

    # def tearDown(self):
    #     Debugging(User.objects.all(), color='yellow')

    async def test_connect(self):
        communicator = WebsocketCommunicator(Alerts.as_asgi(), self.url)
        connected, subprotocol = await communicator.connect()
        assert connected
        await communicator.send_to(text_data="hello")
        response = await communicator.receive_from()
        await communicator.disconnect()

    async def test_send(self):
        communicator = WebsocketCommunicator(Alerts.as_asgi(), self.url)
        connected, subprotocol = await communicator.connect()
        await communicator.send_to(text_data="hello")
        response = await communicator.receive_from()
        await communicator.disconnect()


class AlertsTests(APITestCase):
    def setUp(self):
        date_format = '%Y-%m-%d'
        time_format = '%H:%M:%S'
        d = datetime.datetime
        self.now = d.now().strftime(time_format)
        after_1_h = d.now() + datetime.timedelta(hours=1)
        after_5_h = d.now() + datetime.timedelta(hours=5)
        self.after_1_h = after_1_h.strftime(time_format)
        self.after_5_h = after_5_h.strftime(time_format)

        after_2_h = d.now() + datetime.timedelta(hours=2)
        after_3_h = d.now() + datetime.timedelta(hours=3)
        self.after_2_h = after_2_h.strftime(time_format)
        self.after_3_h = after_3_h.strftime(time_format)

        after_10_h = d.now() + datetime.timedelta(hours=10)
        after_11_h = d.now() + datetime.timedelta(hours=11)
        self.after_10_h = after_10_h.strftime(time_format)
        self.after_11_h = after_11_h.strftime(time_format)

        after_1_d = d.now() + datetime.timedelta(days=1)
        after_3_d = d.now() + datetime.timedelta(days=3)

        self.after_1_d = after_1_d.strftime(date_format)
        self.after_3_d = after_3_d.strftime(date_format)

        DateType.objects.create(name='meeting')
        DateType.objects.create(name='appointment')
        tests_setup_function(self)

    async def test_is_auth(self):
        uri = f'ws://localhost:8000/alerts/?token={self.token}&x=xxx'
        async with websockets.connect(uri) as websocket:
            res = await websocket.recv()
            res = json.loads(res)
            self.assertEqual(len(res), 4)

    async def test_can_see_only_own_data(self):
        uri = f'ws://localhost:8000/alerts/?token={self.token3}'
        async with websockets.connect(uri) as websocket:
            res = await websocket.recv()
            res = json.loads(res)
            self.assertEqual(len(res), 1)

    async def test_fields_filter(self):
        uri = f'ws://localhost:8000/alerts/?token={self.token}&fields=username'
        async with websockets.connect(uri) as websocket:
            res = await websocket.recv()
            res = json.loads(res)
            Debugging(res, color='green')
            # TODO
            # for i in res:
    #             assert 'username' in i
    #             assert 'events' not in i

    # async def test_live_update(self):
    #     uri = f'ws://localhost:8000/alerts/?token={self.token}'
    #     async with websockets.connect(uri) as websocket:
    #         res = await websocket.recv()
    #         res = json.loads(res)
            # P_res = sync_to_async(self.client.post)('/calendars/', {
            #     "title": "first",
            #     "description": "",
            #     "start": self.after_1_d,
            #     "end": self.after_3_d,
            #     "from_time": self.after_1_h,
            #     "to_time": self.after_5_h,
            #     "created_by": 1,
            #     "date_type": 1,
            #     "users": [1],
            #     "recurrence": [
            #         "1 sunday",
            #     ],
            # })
            # self.assertEqual(P_res.status_code, status.HTTP_201_CREATED)


    async def test_queries(self):
        uri = f'ws://localhost:8000/alerts/?token={self.token}&events__title=ddd'
        async with websockets.connect(uri) as websocket:
            res = await websocket.recv()
            res = json.loads(res)
            Debugging(res, color='green')

    def test_dates_notifcations(self):
        DateType.objects.create(name='meeting')
        DateType.objects.create(name='appointment')

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
        # self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # #

        # TODO test target`
        # TODO test filter`ing
