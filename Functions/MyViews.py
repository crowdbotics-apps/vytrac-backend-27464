from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from Functions.debuging import Debugging
from Functions.queryset_filtering import queryset_filtering


def convert_to_list(django_boject):
    flat_object = django_boject.values_list('codename', flat=True)
    return list(flat_object)


class ItemsView(generics.ListAPIView):
    # permission_classes = [IsActive]
    # pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter,)
    search_fields = '__all__'

    def get(self, request, *args, **kwargs):
        context = {'request': request, 'method': 'view'}

        items = queryset_filtering(self.queryset.model, request.GET)
        serializer = self.serializer_class(
            items, context=context, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #
    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'method': 'add', 'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemView(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    MyModel = None

    def get_object(self, pk):
        try:
            return self.MyModel.objects.get(id=pk)
        except self.MyModel.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        context = {'request': request, 'method': 'view', 'pk': pk}
        item = self.get_object(pk)
        serializer = self.serializer_class(item, many=False, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        context = {'request': request, 'method': 'change', 'pk': pk}
        date = self.get_object(pk)
        serializer = self.serializer_class(
            date, context=context, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Recurence cass
REC = (
    # ('from_time', models.TimeField),
    # ('to_time', models.TimeField),
    ('0 month', 'Every month.'),
    ('0 3 month', 'Every 3 months.'),
    ('0 6 month', 'Every 6 months.'),
    ('0 year', 'Every year.'),
    ('1 sunday', 'Every sunday.'),
    ('1 monday', 'Every monday.'),
    ('1 tuesday', 'Every tuesday.'),
    ('1 wednesday', 'Every wednesday.'),
    ('1 thursday', 'Every thursday.'),
    ('1 friday', 'Every friday.'),
    ('1 saturday', 'Every saturday.'),

    #  TODO recurnce on spesifc months
    ('2 january ', 'Every january.'),
    ('2 february', 'Every february.'),
    ('2  march', 'Every march.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 julay', 'Every julay.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),
    # ('2 aprile', 'Every aprile.'),

)


def myfunction(self, *args, **kwargs):
    # TODO maybe add this to the serializer insead of here.
    if str(self).count('0') > 1:
        raise ValidationError(
            _("You should choose one, either every day or every month or every year"), )

    if str(self).count('G') >= 1 and str(self).count('1') >= 1:
        days = list(filter(lambda k: '1' in k, self))
        fD = []
        for day in days:
            fD.append(day.replace('1 ', '').title())
        raise ValidationError(
            _("If it reapeate every day it will repeated on " + str(fD) + " as well"), )


class Rec(MultiSelectField):
    def _choices_is_value(self, *args, **kwargs):
        self.choices = REC
        self.max_length = 93
        self.validators = [myfunction]
        if (len(self.choices) > 2):
            return super()._choices_is_value(*args, **kwargs)
