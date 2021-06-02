from Functions.Myclasses import DynamicSerializer, ItemView, ItemsView
from django.urls import path

from django.contrib.auth.models import Group

MyModel = Group


class GroupSer(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class GroupsView(ItemsView):
    queryset = MyModel.objects.all()
    serializer_class = GroupSer


class GroupView(ItemView):
    queryset = MyModel.objects.all()
    serializer_class = GroupSer


urlpatterns = [
    path('', GroupsView.as_view(), name='groups'),
    path('<int:pk>/', GroupView.as_view(), name='group'),
]


# @receiver(signals , sender=User)
# def my_handler(sender, **kwargs):
#     TODO if 'can_change_smth'in instance.user_permissions then set'can_view_smth'
