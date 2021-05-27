from Myclasses import DynamicSerializer, ItemView, ItemsView
from django.urls import path
from . import models
MyModel = models.PatientProfile


class ItemSer(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


fields = ["id",  "deleted",  "date_created",  "is_active",  "is_adhering",
          "prescriptions",  "created_by",  "user",  "care_taker",  "booked_servces",  "symptoms", ]


class PationtsView(ItemsView):
    queryset = MyModel.objects.all()
    serializer_class = ItemSer
    search_fields = fields
    filterset_fields = fields


class PationtView(ItemView):
    queryset = MyModel.objects.all()
    serializer_class = ItemSer


urlpatterns = [
    path('', PationtsView.as_view(), name='PationtsView'),
    path('<int:pk>/', PationtView.as_view(), name='PationtsView'),
]
