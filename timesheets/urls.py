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

from django.db.models.functions import TruncMonth, TruncMinute,TruncDay
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
        data = ChangeTrack.objects.all()

        fields = [ "id", "deleted", "date_created", "action_type", "model_target", "object_id", "field_target", "field_value", "by"]

        for field in fields:
            q = Q(**{"%s"% field: getter.get(field) })
            if (getter.get(field)!=None):
                data = data.filter(q)

        # if (getter.get('id')!=None):
        #     data = data.filter(id=getter.get('id'))
        # if (getter.get('deleted')!=None):
        #     data = data.filter(deleted=getter.get('deleted'))
        # if (getter.get('date_created')!=None):
        #     data = data.filter(date_created=getter.get('date_created'))
        # if (getter.get('action_type')!=None):
        #     data = data.filter(action_type=getter.get('action_type'))
        # if (getter.get('object_id')!=None):
        #     data = data.filter(object_id=getter.get('object_id'))
        # if (getter.get('field_target')!=None):
        #     data = data.filter(field_target=getter.get('field_target'))
        # if (getter.get('field_value')!=None):
        #     data = data.filter(field_value=getter.get('field_value'))
        # if (getter.get('by')!=None):
        #     data = data.filter(by=getter.get('by'))



        try:
            time_frame = getter.get('time_frame').title()
            target = getter.get('target').lower()
            calttr = getter.get('cal').lower()

            Trunc = getattr(functions, 'Trunc'+time_frame)
            
            cal = getattr(CAL, calttr.title())
            # Avg, F, RowRange, Window, Max, Min
            data = data.annotate(time=Trunc('date_created')).values('time').annotate(avg=cal(target))
            return Response(list(data))
        except:
            return self.list(request, *args, **kwargs)
        
    queryset = MyModel.objects.all()
    serializer_class = StatisticSer
    


class  StatsticView(ItemView):
    queryset = MyModel.objects.all()
    serializer_class = StatisticSer



urlpatterns = [
    # TODO reseave timesheet data data
    # 1. interactions with daly palns
    # 2. clicks or wahtever
    path('', StatsticsView.as_view(), name='Statstics'),
    path('<int:pk>/', StatsticView.as_view(), name=' Statstic'),
]
