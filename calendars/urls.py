from rest_framework import fields, serializers
import datetime
from dateutil import parser
from Myclasses import DynamicSerializer, ItemView, ItemsView, REC
from django.urls import path
from . import models
from rest_framework import response, serializers
from drf_queryfields import QueryFieldsMixin
from users.models import User
import pytz

MyModel = models.Date


def overlap(first_inter, second_inter):
    for f, s in ((first_inter, second_inter), (second_inter, first_inter)):
        for time in (f["i"], f["f"]):
            if s["i"] <= time <= s["f"]:
                return True
    else:
        return False


class DateSer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class CalinderSeriazliser(DynamicSerializer):
    recurrence = fields.MultipleChoiceField(choices=REC)
    # created_by = serializers.CharField(required=False)
    date_created = serializers.CharField(required=False)

    def validate(self, data, *args, **kwargs):
        # TODO add recursive validation logic
        # TODO for i in user.avalable if date not in i reaise 'User can be avalabel in [], user already have dates in []'
        messages = []
        my_format = '%Y-%m-%d'
        my_s_format = 'T%H:%M:%S.%fZ'
        now = datetime.datetime.now().strftime(my_format)
        # data['created_by'] = self.context['request'].user
        # created_by = data['created_by']
        data['date_created'] = now
        title = data['title']
        description = data['description']
        users = data['users']
        G_overlap = False
        S_overlap = False
        Rec_overlap = False

        recurrence = data['recurrence']
        from_time = data['from_time'].strftime(my_s_format)
        to_time = data['to_time'].strftime(my_s_format)
        start = data['start'].strftime(my_format)
        end = data['end'].strftime(my_format)

        date_type = data['date_type']
        dates = MyModel.objects.all()
        dates = dates.filter(start__gte=now, end__gte=now)
        dates = dates.filter(users__in=users)

        for date in dates:
            date1 = {}
            date2 = {}
            date1['i'] = date.start.strftime(my_format)
            date1['f'] = date.end.strftime(my_format)
            date2['i'] = start
            date2['f'] = end
            if (overlap(date1, date2)):
                G_overlap = True

        for date in dates:
            date1 = {}
            date2 = {}
            date1['i'] = date.from_time.strftime(my_s_format)
            date1['f'] = date.to_time.strftime(my_s_format)
            date2['i'] = from_time
            date2['f'] = to_time
            if (overlap(date1, date2)):
                S_overlap = True

        for date in dates:
            if bool(set(date.recurrence) & set(data['recurrence'])):
                Rec_overlap = True

        # for date in dates:
        #     TODO if (('G' in date.recurrence) and ('G' or "1 " in (data['recurrence'])):
        #         Rec_overlap = True

        # for date in dates:
        #     TODO if (('G'or 'i' in date.recurrence) and ('G' in (data['recurrence'])):
        #         Rec_overlap = True

        if (G_overlap and Rec_overlap and S_overlap):
            raise serializers.ValidationError(
                {'overlap error': 'The date you entered overlap with som of the existed dates',
                 # TODO 'overlap with': DateSer(date, many=False).data,
                 'existed dates': DateSer(dates, many=True).data})

        # TODO do the same logic in function for avalibality
        #  if (not G_overlap and not Rec_overlap and not S_overlap):
        #     messages.append(user.username+' is not avalble at this time')

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
        # if (not created_by.is_staff or not created_by.is_superuser):
        #     users.append(created_by)

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


# del ItemsView.post
class CalindersView(ItemsView):
    ModelName = 'date'
    queryset = MyModel.objects.all()
    serializer_class = CalinderSeriazliser


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
