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
        data = super().get(request, *args, **kwargs).data
        getter = request.GET
        if 'cal' in getter and 'fields' in getter:
            return Response({'error': 'You can not element fields because thy are needed for th calculations'},
                            status=status.HTTP_400_BAD_REQUEST)

        if getter.get('resample') is not None and getter.get('cal') is not None:
            resample = getter.get('resample').title()
            clatter = getter.get('cal').lower()
            df = pd.DataFrame(data)
            df['date_created'] = pd.to_datetime(df['date_created'])

            df = df.groupby('field_target').apply(
                lambda x: getattr(x.set_index('date_created').resample(resample), clatter)())
            # df = df.reset_index().to_dict('records')
            # Debugging(df, color='red')
            return Response(data, status=status.HTTP_200_OK)  # todo self.list() for filtering
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
