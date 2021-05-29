from Myclasses import DynamicSerializer, ItemView, ItemsView
from django.urls import path
from . import models
MyModel = models.PatientProfile


class ItemSer(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class PationtsView(ItemsView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ItemSer


class PationtView(ItemView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ItemSer


urlpatterns = [
    path('', PationtsView.as_view(), name='PationtsView'),
    path('<int:pk>/', PationtView.as_view(), name='PationtsView'),
]
