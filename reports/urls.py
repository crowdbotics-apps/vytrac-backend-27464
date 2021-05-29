from Myclasses import DynamicSerializer, ItemView, ItemsView
from django.urls import path
from . import models
MyModel = models.Report


class ItemSer(DynamicSerializer):
    def validate(self, *args, **kwargs):
        # for setting in user.settings:
        #     if not settings.see_all:
        #         return self.Reports.filter(realted_to=user) # or self.data
        return super().validate(args, kwargs)

    class Meta:
        model = MyModel
        fields = '__all__'


class ReportsView(ItemsView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ItemSer


class ReportView(ItemView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ItemSer


urlpatterns = [
    path('', ReportsView.as_view(), name='Reports'),
    path('<int:pk>/', ReportView.as_view(), name='Report'),
]
