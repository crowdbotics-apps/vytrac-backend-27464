import sys
from Functions.debuging import Debugging
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
    # notifications = Notifications.objects.filter(
    #     Q(target_users__in=[user.id]) or Q(target_groups__in=user.groups.all()))
    # if (user.is_staff or user.is_superuser):
    #     notifications = Notifications.objects.all()
    return Notifications.objects.all()


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
        Debugging('disconnect====================== ', color='red')
        print(close_code)
        print(self)

    def receive(self, text_data):
        Debugging('receive======================', color='green')
        errors = []

        user = self.scope["user"]
        data = json.loads(text_data)

        notifcation = return_notifcations(
            Notifications, user).get(id=data['id'])

        fields = [x.name for x in notifcation._meta.fields]
        if data['field'] not in fields:
            errors.append(
                {'Field name error.': 'The field you entered is not exist.'})

        try:
            setattr(notifcation, data['field'], data['value'].title())
            notifcation.save()
        except Exception as e:
            errors.append(str(e))

        if (len(errors) == 0):
            serializer = serializers.ItemsSer(
                return_notifcations(Notifications, user), many=True)
            x = json.dumps({'message': serializer.data})
            self.send(x)
        else:
            self.send(json.dumps({'errors': errors}))

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
