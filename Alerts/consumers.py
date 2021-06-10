import json

from channels.generic.websocket import WebsocketConsumer
from rest_framework import serializers

from Functions.debuging import Debugging
from Functions.queryset_filtering import queryset_filtering
from patients.models import Patient
from users import models


class Myser(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'id', 'dates']
        depth = 1


from urllib.parse import parse_qs



def return_notifcations(scope):
    ids = []
    user = scope.get('user')
    queries = scope['query_string']
    queries = parse_qs(queries.decode("utf8"))
    patients = queryset_filtering(Patient, queries)
    users = queryset_filtering(Patient, queries)
    # changeTracker = queryset_filtering(Column, queries)

    # ids.append(items.values('id'))
    # users = models.User.objects.filter(id__in=[1])
    users = models.User.objects.all()


    # if user.is_staff or user.is_superuser:
    #     users = models.User.objects.all()
    data = Myser(users,
                 many=True, context=scope).data
    # for date in data['dates']:
    #     date['is_seen'] = user.id in date['seen_by']
    return json.dumps({'message': data})


class Alerts(WebsocketConsumer):

    def connect(self):
        user = self.scope.get('user')
        # notifcation = return_notifcations(self.scope)
        self.accept()
        self.send('notifcation')

    def receive(self, text_data):
        errors = []
        user = self.scope.get('user')
        # data = json.loads(text_data)
        # TODO date= Date.objects.get(id=data.id)
        # date = date.seen_by.add(user)
        # notifcation = return_notifcations(self.scope)
        # self.send(notifcation)

        notifcation = return_notifcations(self.scope)

    def disconnect(self, close_code):
        print(close_code)
        print(self)




