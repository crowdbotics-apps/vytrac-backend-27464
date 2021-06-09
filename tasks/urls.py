from django.urls import path

from Functions.DynamicSer import DynamicSerializer
from Functions.MyViews import ItemView, ItemsView
from .models import Tasks

MyModel = Tasks


class ItemSer(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class TasksView(ItemsView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ItemSer


class TaskView(ItemView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ItemSer


urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('<int:pk>/', TaskView.as_view(), name='task'),
]
