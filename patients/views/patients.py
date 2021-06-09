from rest_framework import status, serializers
from rest_framework.response import Response

from Functions.DynamicSer import DynamicSerializer
from Functions.MyViews import ItemView, ItemsView
from .. import models

MyModel = models.Patient

class emergency_contact_ser(serializers.ModelSerializer):
    class Meta:
        model = models.EmergencyContact
        exclude = ['patient']

class ModelSer(DynamicSerializer):

    emergency_contact = emergency_contact_ser(models.EmergencyContact,many=True, required=False,read_only=True)

    class Meta:
        model = MyModel
        fields = '__all__'
        depth = 1


class PostModelSer(DynamicSerializer):

    class Meta:
        model = MyModel
        fields = '__all__'

class Views(ItemsView):
    queryset = MyModel.objects.all()
    serializer_class = ModelSer


class View(ItemView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ModelSer
