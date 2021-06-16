import difflib

from django.urls import path
from rest_framework import status, serializers
from rest_framework.response import Response

from Functions.DynamicSer import DynamicSerializer
from Functions.MyViews import ItemView, ItemsView
from Functions.debuging import Debugging
from Functions.fields_lookups import fields_lookups
from users.models import User
from .Functions.Statstics import statistics
from .models import Value, Column

MyModel = Value


# Debugging(Value.objects.filter(column__name='vv'), color='green')
# Debugging(Value.objects.all(), color='green')


class ColumnSer(DynamicSerializer):
    class Meta:
        model = Column
        fields = ['name', 'user', ]


class StatisticSer(DynamicSerializer):
    column = ColumnSer(many=False, read_only=True, required=False)

    class Meta:
        model = MyModel
        fields = ['field_value', 'name', 'action', 'seen_by', 'date_created', 'column']


class Postser(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class StatsticsView(ItemsView):
    def get(self, request, *args, **kwargs):
        data = super().get(request, *args, **kwargs).data
        getter = request.GET

        if ('cal' in getter) and ('fields' in getter):
            return Response({'error': 'You can not element fields because thy are needed for th calculations'},status=status.HTTP_400_BAD_REQUEST)

        data = statistics(data, getter)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        column = request.data.get('column')
        is_sure = request.data.get('sure')
        cal_name = request.data['column']['name']

        words = []
        for col in Column.objects.all():
            if cal_name != col.name:
                words.append(col.name)
        words = difflib.get_close_matches(cal_name, words)
        if len(words) > 0 and is_sure != "true":
            return Response({
                'potential typo': 'Did you mean ' + str(words) + '?',
                "note": "If you think you do not have a typo send {'sure' : 'true'} with the data."})

        column, created = Column.objects.get_or_create(name=column, user=User.objects.get(id=1))
        request.data['column'] = column.id
        self.serializer_class = Postser
        return super().post(request, *args, **kwargs)

    queryset = MyModel.objects.all()
    serializer_class = StatisticSer


class StatsticView(ItemView):
    queryset = MyModel.objects.all()
    serializer_class = StatisticSer


urlpatterns = [
    path('', StatsticsView.as_view(), name='Statstics'),
    path('<int:pk>/', StatsticView.as_view(), name=' Statstic'),

]
