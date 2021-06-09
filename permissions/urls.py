from django.contrib.auth.models import Group
from django.urls import path
from Functions.DynamicSer import DynamicSerializer
from Functions.MyViews import ItemView, ItemsView

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


# @Receiver(signals , sender=User)
# def my_handler(sender, **kwargs):
#     TODO if 'can_change_smth'in instance.user_permissions then set'can_view_smth'
