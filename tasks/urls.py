from django.urls import path
from Myclasses import DynamicSerializer, ItemView, ItemsView
from django.urls import path
from . import models
MyModel = models.Tasks


class ItemSer(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class TasksView(ItemsView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ItemSer
    # TODO
    # def get():
    # tasks = Itams.objects.filter(user=request.user)
    #     return {'tasks':tasks, 'items':Items}


class TaskView(ItemView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ItemSer


urlpatterns = [
    path('', TasksView.as_view(), name='tasks'),
    path('<int:pk>/', TaskView.as_view(), name='task'),
]
