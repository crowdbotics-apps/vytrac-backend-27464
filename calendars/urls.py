import datetime
from dateutil import parser
from Myclasses import DynamicSerializer, ItemView, ItemsView
from django.urls import path
from . import models
from rest_framework import response, serializers
from drf_queryfields import QueryFieldsMixin
from users.models import User
import pytz

MyModel = models.Date


def overlap(first_inter, second_inter):
    for f, s in ((first_inter, second_inter), (second_inter, first_inter)):
        for time in (f["starting_time"], f["ending_time"]):
            if s["starting_time"] < time < s["ending_time"]:
                return True
    else:
        return False


class DateSer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class CalinderSeriazliser(DynamicSerializer):
    created_by = serializers.CharField(required=False)
    date_created = serializers.CharField(required=False)

    def validate(self, data, *args, **kwargs):
        messages = []
        my_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        now = datetime.datetime.now().strftime(my_format)
        data['created_by'] = self.context['request'].user
        created_by = data['created_by']
        data['date_created'] = now
        title = data['title']
        description = data['description']
        users = data['users']
        start = data['start'].strftime(my_format)
        end = data['end'].strftime(my_format)
        date_type = data['date_type']
        dates = models.Date.objects.all()
        dates = dates.filter(start__gte=now, end__gte=now)
        dates = dates.filter(users__in=users)
        for date in dates:
            date1 = {}
            date2 = {}
            date1['starting_time'] = date.start.strftime(my_format)
            date1['ending_time'] = date.end.strftime(my_format)
            date2['starting_time'] = start
            date2['ending_time'] = end
            if (overlap(date1, date2)):
                raise serializers.ValidationError(
                    {'overlap error': 'The date you entered overlap with som of the existed dates', 'overlap with': DateSer(date, many=False).data, 'existed dates': DateSer(dates, many=True).data})

        # if (intersected()):
        #     raise serializers.ValidationError({'users are busy during':
        #     list_of_all_dates})
        if (date_type.name[0] in ['i', '0', 'u', 'a', 'e']):
            date_type.name = 'an '+date_type.name
        else:
            date_type.name = 'a '+date_type.name

        if (len(users) < 2 and date_type == 'appointment'):
            raise serializers.ValidationError(
                'At least two people shoul have an appointment.')
        if((start or end) <= now):
            raise serializers.ValidationError(
                "You can't have "+date_type.name+" start or end before now.")

        if (start >= end):
            raise serializers.ValidationError(
                "Start date must be before the end date.")
        if (not created_by.is_staff or not created_by.is_superuser):
            users.append(created_by)

        return data
        # start_date = pytz.UTC.localize(parser.parse(request.data['start']))
        # end_date = pytz.UTC.localize(parser.parse(request.data['end']))
        # users_list = request.data.getlist('users')
        # date_type = ''
        # try:
        #     date_type = models.DateType.objects.get(
        #         id=request.data['date_type']).name
        # except:
        #     pass
        # if (not request.user.is_staff or not request.user.is_superuser):
        #     users_list.append(request.user.id)
        # busy_schadules = models.Date.objects.filter(
        #     start__gte=request.data['start'], end__gte=request.data['end'])
        # for busy_schadule in busy_schadules:
        # return super().post(request, *args, **kwargs)

    class Meta:
        model = MyModel
        fields = '__all__'


fields = ["id", "deleted", "title", "description", "start",
          "end", "date_created", "date_type", "created_by", "users", ]


class CalindersView(ItemsView):
    ModelName = 'date'
    queryset = MyModel.objects.all()
    serializer_class = CalinderSeriazliser
    search_fields = fields
    filterset_fields = fields

    # def post(self, request, *args, **kwargs):
    #     start_date = pytz.UTC.localize(parser.parse(request.data['start']))
    #     end_date = pytz.UTC.localize(parser.parse(request.data['end']))
    #     messages = []
    #     users_list = request.data.getlist('users')
    #     date_type = ''
    #     try:
    #         date_type = models.DateType.objects.get(
    #             id=request.data['date_type']).name
    #     except:
    #         pass
    #     if (not request.user.is_staff or not request.user.is_superuser):
    #         users_list.append(request.user.id)
    #     busy_schadules = models.Date.objects.filter(
    #         start__gte=request.data['start'], end__gte=request.data['end'])
    #     for busy_schadule in busy_schadules:
    #     return super().post(request, *args, **kwargs)


class CalinderView(ItemView):
    ModelName = 'date'
    queryset = MyModel.objects.all()
    serializer_class = CalinderSeriazliser


urlpatterns = [
    path('', CalindersView.as_view(), name="calinders"),
    path('<int:pk>/', CalinderView.as_view(), name="calinder"),
    # path('', TypesView.as_view(), name="date_types"),
    # path('<int:pk>/', TyperView.as_view(), name="date_type"),
]
