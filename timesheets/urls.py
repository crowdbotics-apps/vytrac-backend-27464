import pandas as pd
from django.urls import path
from rest_framework import status
from rest_framework.response import Response

from Functions.DynamicSer import DynamicSerializer
from Functions.MyViews import ItemView, ItemsView
from Functions.debuging import Debugging
from Functions.fields_lookups import fields_lookups
from .models import ChangeTrack

MyModel = ChangeTrack



class StatisticSer(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class StatsticsView(ItemsView):
    def get(self, request, *args, **kwargs):
        context = {'request': request, 'method': 'view'}
        items = self.queryset.all()
        serializer = self.serializer_class(items, context=context, many=True)
        data = serializer.data
        # Debugging(data, color='green')

        getter = request.GET

        if getter.get('resample') is not None and getter.get('cal') is not None:
            resample = getter.get('resample').title()
            target = getter.get('target').lower()
            clatter = getter.get('cal').lower()
            df = pd.DataFrame(data)
            df['date_created'] = pd.to_datetime(df['date_created'])

            df = df.groupby('field_target').apply(
                lambda x: getattr(x.set_index('date_created').resample(resample), clatter)())
            return Response(df, status=status.HTTP_200_OK) #todo self.list() for filtering

        return Response(data, status=status.HTTP_200_OK)

    queryset = MyModel.objects.all()
    serializer_class = StatisticSer
    filterset_fields = fields_lookups(MyModel)


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
