import gc
from channels.generic.websocket import WebsocketConsumer
import json
from django.dispatch import receiver
from django.db.models import signals
from .models import Notifications
from . import serializers


def return_notifcations(user):
    # TODO
    notifcations1 = Notifications.objects.filter(target_users__in=user)
    notifcations2 = Notifications.objects.filter(target_groups__in=user.groups)
    notifcations = notifcations1+notifcations2
    return notifcations


class WSConsumer(WebsocketConsumer):
    # def websocket_connect(self):
    #     # self.user = self.scope["user"]
    #     # user = self.scope["user"]
    #     self.accept()

    def connect(self):
        # TODO A3
        #notifcations =  Notifications.objects.filter(target_users__contains=self.scope['user'])
        # notifcations.filter(target_groups__contains=self.scope['user'].groups)
        # filter by scope["query_string"]
        # 1. notifcation/?importance=high,meduim
        # 2. notifcation/?title=appointment,interveiw
        #
        self.accept()
        serializer = serializers.ItemsSer(
            Notifications.objects.all(), many=True)
        x = json.dumps({'message': serializer.data})
        self.send(x)

        @receiver(signals.post_save, sender=Notifications)
        def __init__(instance, sender, signal, *args, **kwargs):
            serializer = serializers.ItemsSer(
                sender.objects.all(), many=True)
            x = json.dumps({'message': serializer.data})
            self.send(x)

        # print(self.scope["user"].username)

        # for i in range(10):
        #     x = json.dumps({'message': i})
        #     self.send(x)
        #     sleep(0.3)
