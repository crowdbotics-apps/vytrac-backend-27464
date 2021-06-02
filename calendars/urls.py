from rest_framework import fields, serializers
import datetime
from dateutil import parser
from Functions.Myclasses import DynamicSerializer, ItemView, ItemsView, REC
from django.urls import path
from . import models
from rest_framework import serializers

MyModel = models.Date


def is_overlap(date_item, date_set):
    date_format = '%Y-%m-%d'
    time_format = 'T%H:%M:%S.%fZ'
    G_overlap = False
    S_overlap = False
    Rec_overlap = False

    def overlap(first_inter, second_inter):
        for f, s in ((first_inter, second_inter), (second_inter, first_inter)):
            for time in (f["i"], f["f"]):
                if s["i"] <= time <= s["f"]:
                    return True
        else:
            return False

    for date in date_set:
        date1 = {}
        date2 = {}
        date1['i'] = getattr(date, 'start').strftime(date_format)
        date1['f'] = getattr(date, 'end').strftime(date_format)
        date2['i'] = date_item['start'].strftime(date_format)
        date2['f'] = date_item['end'].strftime(date_format)
        if (overlap(date1, date2)):
            G_overlap = True

        time1 = {}
        time2 = {}
        time1['i'] = getattr(date, 'from_time').strftime(date_format)
        time1['f'] = getattr(date, 'to_time').strftime(date_format)
        time2['i'] = date_item['from_time'].strftime(date_format)
        time2['f'] = date_item['to_time'].strftime(date_format)
        if (overlap(time1, time2)):
            S_overlap = True

        lengths = [len(date.recurrence), len(date_item['recurrence'])]
        if (0 in lengths):
            if (S_overlap and G_overlap and '0 G day' in str(date_item['recurrence'])):
                Rec_overlap = True

        if (lengths[0] == 0 and lengths[1] == 0):
            if (S_overlap and G_overlap):
                Rec_overlap = True

        if (bool(set(date.recurrence) & set(date_item['recurrence']))):
            Rec_overlap = True

        # print('======================')
        # print(Rec_overlap)
        # print(G_overlap)
        # print(S_overlap)
        # print('======================')

        # TODO if bool(set(['0 G day']) & set(date['recurrence'])) and any("1 " in s for s in date_item['recurrence']):
        #     Rec_overlap = True

        # TODO if bool(set(['1 ']) & set(date['recurrence'])) and any("0 G day " in s for s in date_item['recurrence']):
        #     Rec_overlap = True

    return Rec_overlap and S_overlap and G_overlap


class DateSer(serializers.ModelSerializer):
    # TODO recurrence = serializers.ChoiceField(Required=False)

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
        today = datetime.datetime.now().strftime(my_format)
        # data['created_by'] = self.context['request'].user
        # created_by = data['created_by']
        data['date_created'] = today
        users = data['users']
        start = data['start'].strftime(my_format)
        end = data['end'].strftime(my_format)

        date_type = data['date_type']
        dates = MyModel.objects.all()
        dates = dates.filter(start__gte=today, end__gte=today)
        dates = dates.filter(users__in=users)

        if (is_overlap(data, dates)):
            raise serializers.ValidationError(
                {'overlap error': 'The date you entered overlap with som of the existed dates',
                 # TODO 'overlap with': DateSer(date, many=False).data,
                 'existed dates': DateSer(dates, many=True).data})
        if ('0 G day' in str(data['recurrence']) and '1 ' in str(data['recurrence'])):
            days = list(filter(lambda x: '1 ' in x, list(data['recurrence'])))
            parse_days = list(
                filter(lambda x: x.replace('1 ', '').title(), days))
            raise serializers.ValidationError(
                {'logic error': 'If avery day then it is already every '+str(parse_days)})

        # TODO if (is_overlap(date,dates)):
        #     raise serializers.ValidationError(
        #         {'overlap error': 'The date you entered overlap with som of the existed dates',
        #          # TODO 'overlap with': DateSer(date, many=False).data,
        #          'existed dates': DateSer(dates, many=True).data})

        # TODO do the same logic in function for avalibality
        # for user in users:
        #  if (not is_overlap(date,user.avalibity)):
        #     messages.append(user.username+' is not avalble at this time')

        if (date_type.name[0] in ['i', '0', 'u', 'a', 'e']):
            date_type.name = 'an '+date_type.name
        else:
            date_type.name = 'a '+date_type.name

        if (len(users) < 2 and date_type == 'appointment'):
            raise serializers.ValidationError(
                'At least two people shoul have an appointment.')
        if((start or end) <= today):
            raise serializers.ValidationError(
                "You can't have "+date_type.name+" start or end before today.")

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
