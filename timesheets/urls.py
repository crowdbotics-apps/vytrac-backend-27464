from re import DEBUG
from django.urls import path
from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers
from .models import ChangeTrack


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
    def get(self, request, *args, **kwargs):
        getter = request.GET
        data = MyModel.objects.all()

        query = Q()
        fields = []
        for field in MyModel._meta.fields:
            for s in list(getter):
                if field.name in s:
                    fields.append(s)

        for field in fields:
            q = Q(**{"%s" % field: getter.get(field)})
            if (getter.get(field) != None):
                query &= q
        data = data.filter(query)
        # print('xxx======================')
        # print(list(data))
        # print(query)
        # print('======================')
        if (getter.get('time_frame') != None):
            try:

                time_frame = getter.get('time_frame').title()
                target = getter.get('target').lower()
                calttr = getter.get('cal').lower()

                Trunc = getattr(functions, 'Trunc'+time_frame)
                cal = getattr(CAL, calttr.title())
                # Avg, F, RowRange, Window, Max, Min
                data = data.annotate(time=Trunc('date_created')).values(
                    'time').annotate(avg=cal(target))
                return Response(list(data))
            except:
                pass
        return self.list(data)

    queryset = MyModel.objects.all()
    serializer_class = StatisticSer


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
