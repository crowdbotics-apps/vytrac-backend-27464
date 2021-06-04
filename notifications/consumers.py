import json

from channels.generic.websocket import WebsocketConsumer
from django.db.models import signals
from django.dispatch import receiver
from rest_framework import serializers

from Functions.debuging import Debugging
from users import models
from .models import Notifications


class Myser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'id', 'dates']
        depth = 1


def return_notifcations(scope):
    user = scope['user']
    data = Myser(models.User.objects.get(id=user.id),
                 many=False, context=scope).data
    for date in data['dates']:
        date['is_seen'] = user.id in date['seen_by']
    return json.dumps({'message': data})


class Alerts(WebsocketConsumer):

    def disconnect(self, close_code):

        Debugging('disconnect====================== ', color='red')
        print(close_code)
        print(self)

    def receive(self, text_data):
        Debugging('receive======================', color='green')
        errors = []
        user = self.scope["user"]
        data = json.loads(text_data)
        # TODO date= Date.objects.get(id=data.id)
        #date = date.seen_by.add(user)
        notifcation = return_notifcations(self.scope)
        self.send(notifcation)

        notifcation = return_notifcations(self.scope)

    def connect(self):
        user = self.scope["user"]
        notifcation = return_notifcations(self.scope)
        self.accept()
        self.send(notifcation)

        # TODO A3
        #notifcations =  Notifications.objects.filter(target_users__contains=self.scope['user'])
        # notifcations.filter(target_groups__contains=self.scope['user'].groups)
        # filter by scope["query_string"]
        # 1. notifcation/?importance=high,meduim
        # 2. notifcation/?title=appointment,interveiw
        #

        @receiver(signals.post_save, sender=Notifications)
        def __init__(instance, sender, signal, *args, **kwargs):

            x = json.dumps({'message': 'data'})
            self.send(x)
            pass
