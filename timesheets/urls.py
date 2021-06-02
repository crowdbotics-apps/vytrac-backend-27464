import inspect
from Functions.fields_lookups import fields_lookups
from Functions.debuging import Debugging
from django.db.models.query_utils import DeferredAttribute
from django_filters.rest_framework.backends import DjangoFilterBackend
import pandas as pd
from re import DEBUG
from typing import SupportsAbs
from django.db.models.lookups import Contains
from django.urls import path
from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers
from .models import ChangeTrack
from itertools import groupby
from operator import itemgetter


from Functions.Myclasses import DynamicSerializer, ItemView, ItemsView
from django.urls import path
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, mixins, permissions
from rest_framework.response import Response
from Functions.MyFunctions import permision_chack
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from users.models import User

from django.db.models.functions import TruncMonth, TruncMinute, TruncDay
from django.db.models import Count
from django.db.models import functions

from django.db.models.functions import Extract, Cast
from django.db import models as CAL


MyModel = ChangeTrack


class StatisticSer(DynamicSerializer):
    # super().post(request, *args, **kwargs)
    class Meta:
        model = MyModel
        fields = '__all__'


class StatsticsView(ItemsView):
    queryset = MyModel.objects.all()
    serializer_class = StatisticSer
    filterset_fields = fields_lookups(MyModel)

    def get(self, request, *args, **kwargs):
        getter = request.GET
        data = request.data
        data = self.list(data, args, kwargs).data

        if (getter.get('resample') != None and getter.get('cal') != None):
            resample = getter.get('resample').title()
            target = getter.get('target').lower()
            calttr = getter.get('cal').lower()

            df = pd.DataFrame(data)

            df['date_created'] = pd.to_datetime(df['date_created'])

            df = df.groupby('field_target').apply(
                lambda x: getattr(x.set_index('date_created').resample(resample), calttr)())

            return Response(df)

        return Response(data)


class StatsticView(ItemView):
    queryset = MyModel.objects.filter(id=2)
    serializer_class = StatisticSer


urlpatterns = [
    # TODO reseave timesheet data data
    # 1. interactions with daly palns
    # 2. clicks or wahtever
    path('', StatsticsView.as_view(), name='Statstics'),
    path('<int:pk>/', StatsticView.as_view(), name=' Statstic'),


]
