from Myclasses import ItemView, ItemsView
from django.urls import path
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from MyFunctions import permision_chack
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from users.models import User
from . import models
from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin

from . import models
MyModel = models.Payment


class paymentsSer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class BillginsView(ItemsView):
    ModelName = 'payment'
    queryset = MyModel.objects.all()
    serializer_class = paymentsSer


class BillginView(ItemView):
    ModelName = 'payment'
    queryset = MyModel.objects.all()
    serializer_class = paymentsSer


urlpatterns = [
    path('', BillginsView.as_view(), name='billings'),
    path('<int:pk>/', BillginView.as_view(), name='billgin'),
]
