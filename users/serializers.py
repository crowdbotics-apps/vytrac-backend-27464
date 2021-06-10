from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
)

from Functions.DynamicSer import DynamicSerializer
from patients.views import patients
from timesheets.urls import StatisticSer
from .models import User, Availablity


class AvalibitlySer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field='username')

    class Meta:
        model = Availablity
        fields = '__all__'



class UserUpdateSer(ModelSerializer):
    username = serializers.CharField(max_length=555)

    class Meta:
        fields = ['username', ]


class UpdateSer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'name',
            'designation',
            'is_active',
            'is_superuser',
            'is_staff',
        )



class UsersSerializer(DynamicSerializer):
    statistics = StatisticSer(many=True,read_only=True)
    patient_profile = patients.ModelSer(many=False, read_only=True)
    class Meta:
        model = User
        fields = [*[x.name for x in User._meta.fields], 'dates','statistics','patient_profile']
        depth = 1
