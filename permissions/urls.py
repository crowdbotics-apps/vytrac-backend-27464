from Myclasses import DynamicSerializer, ItemView, ItemsView
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
from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from django.contrib.auth.models import Group

MyModel = Group


class GroupSer(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class GroupsView(ItemsView):
    queryset = MyModel.objects.all()
    serializer_class = GroupSer


class GroupView(ItemView):
    queryset = MyModel.objects.all()
    serializer_class = GroupSer


urlpatterns = [
    path('', GroupsView.as_view(), name='groups'),
    path('<int:pk>/', GroupView.as_view(), name='group'),
]
