from channels.generic.websocket import WebsocketConsumer
import json
from django.dispatch import receiver
from django.db.models import signals
from rest_framework.fields import DateTimeField
from .models import Notifications
from . import serializers
from django.db.models import Q
import datetime


def return_notifcations(Notifications, user):
    notifications = Notifications.objects.filter(target_users__in=[user.id])
    if (user.is_staff or user.is_superuser):
        notifications = Notifications.objects.all()
    return notifications


class Alerts(WebsocketConsumer):
    # def websocket_connect(self):
    #     # self.user = self.scope["user"]
    #     # user = self.scope["user"]
    #     self.accept()

    def disconnect(self, close_code):
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        print('disconnect======================')
        print(close_code)
        print(self)
        print('======================')

    def receive(self, text_data):
        user = self.scope["user"]
        data = json.loads(text_data)
        print('receive======================')
        errors = []
        notifcation = return_notifcations(
            Notifications, user).filter(id=data['id'])

        if('is_seen' not in data):
            errors.append(
                {'field name error': 'One of field names is not recognized.'})

        if (not notifcation.exists()):
            errors.append(
                {'permission error': 'You are not permisted to update this alert.'})
        try:
            if (notifcation.filter(is_seen=True).exists() and data['is_seen'].title() == 'True'):
                errors.append({'value error': 'value already seted to true'})
        except:
            pass

        if(len(errors) >= 0):
            message = json.dumps({'error': errors})
            self.send(message)

        if(len(errors) == 0):
            notifcation.update(is_seen=True)
            # TODO response_time = notifcation.date_created - datetime.datetime.now()
            # print('======================')
            # print(response_time)
            # print('======================')
            notifcation.save()
            notifcation.response_time = DateTimeField.timedelta(
                days=20, hours=10)
            serializer = serializers.ItemsSer(
                return_notifcations(Notifications, user), many=True)
            x = json.dumps({'message': serializer.data})
            self.send(x)

    def connect(self):
        # TODO return notifcations pased on user settings
        # ex: if provider whatn to see only his realted pationtes
        print('connect======================')
        print(self)
        print('======================')
        user = self.scope["user"]

        # TODO A3
        #notifcations =  Notifications.objects.filter(target_users__contains=self.scope['user'])
        # notifcations.filter(target_groups__contains=self.scope['user'].groups)
        # filter by scope["query_string"]
        # 1. notifcation/?importance=high,meduim
        # 2. notifcation/?title=appointment,interveiw
        #

        self.accept()
        serializer = serializers.ItemsSer(
            return_notifcations(Notifications, user), many=True)
        x = json.dumps({'message': serializer.data})
        self.send(x)

        @receiver(signals.post_save, sender=Notifications)
        def __init__(instance, sender, signal, *args, **kwargs):
            # TODO check self if work
            serializer = serializers.ItemsSer(
                return_notifcations(sender, user), many=True)
            x = json.dumps({'message': serializer.data})
            self.send(x)

        # print(self.scope["user"].username)

        # for i in range(10):
        #     x = json.dumps({'message': i})
        #     self.send(x)
        #     sleep(0.3)
