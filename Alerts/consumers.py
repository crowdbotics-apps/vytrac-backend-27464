import json
from urllib.parse import parse_qs

from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers
from rest_framework_simplejwt.tokens import UntypedToken

from Functions.debuging import Debugging
from Functions.queryset_filtering import queryset_filtering
from calendars.models import Event
from patients.models import Patient
from users import models


class Myser(QueryFieldsMixin,serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'id', 'events']
        depth = 1


class Eventser(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


def return_notifcations(scope):
    # context = {'request': scope, 'method': 'view'}
    ids = []
    user = scope.get('user')
    queries = scope['query_string']
    queries = parse_qs(queries.decode("utf8"))
    for i in queries.keys():
        queries[i] = queries[i][0]


    users = queryset_filtering(models.User, queries)
    if user:
        if not user.is_staff or not user.is_superuser:
            users = users.filter(id=user.id)
    serializer = Myser(users, many=True)
    Debugging(users, color='green')

    return json.dumps(serializer.data)


def get_user(querys):
    token = parse_qs(querys.decode("utf8"))['token'][0]
    token_data = UntypedToken(token)
    user_id = token_data["user_id"]
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()


class Alerts(WebsocketConsumer):
    def connect(self):
        self.accept()
        user = self.scope.get('user')
        if not user:
            self.send('You are not authenticated')
            super().disconnect(self)

        @receiver(post_save, sender=Patient)
        @receiver(post_save, sender=Event)
        def __init__(sender,instance,created, **kwargs):
            if sender.__name__ == 'Event':
                pass
                # self.send(Eventser(instance,many=False).data)
            # Debugging(User.objecs.fields(events__title='ddd'), color='green')
            self.send(return_notifcations(self.scope))

        self.send(return_notifcations(self.scope))

    def receive(self, text_data):
        errors = []
        user = self.scope.get('user')
        # data = json.loads(text_data)
        # TODO date= Date.objects.get(id=data.id)
        # date = date.seen_by.add(user)
        # notifcation = return_notifcations(self.scope)
        # self.send(notifcation)

        # notifcation = return_notifcations(self.scope)

    def disconnect(self, close_code):
        print(close_code)
        print(self)
