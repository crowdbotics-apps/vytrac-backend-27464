import gc
from channels.generic.websocket import WebsocketConsumer
import json
from django.dispatch import receiver
from django.db.models import signals
from .models import Notifications
from . import serializers


def return_notifcations(Notifications,user):
    notes1 = Notifications.objects.filter(target_groups__in=user.groups.all())
    notes2 = Notifications.objects.filter(target_users__in=[user])
    if (user.is_staff or user.is_superuser):
        return Notifications.objects.all()
    return list(notes1)+list(notes2)


class WSConsumer(WebsocketConsumer):
    # def websocket_connect(self):
    #     # self.user = self.scope["user"]
    #     # user = self.scope["user"]
    #     self.accept()

    def connect(self):
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
            return_notifcations(Notifications,user) , many=True)
        x = json.dumps({'message': serializer.data})
        self.send(x)

        @receiver(signals.post_save, sender=Notifications)
        def __init__(instance, sender, signal, *args, **kwargs):
            serializer = serializers.ItemsSer(
                return_notifcations(sender,user), many=True)
            x = json.dumps({'message': serializer.data})
            self.send(x)

        # print(self.scope["user"].username)

        # for i in range(10):
        #     x = json.dumps({'message': i})
        #     self.send(x)
        #     sleep(0.3)
