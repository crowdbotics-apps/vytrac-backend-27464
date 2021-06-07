from Functions.MyViews import ItemView, ItemsView
from .. import models
from Functions.DynamicSer import DynamicSerializer


MyModel = models.Roster


class ModelSer(DynamicSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class Views(ItemsView):
    queryset = MyModel.objects.all()
    serializer_class = ModelSer


class View(ItemView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ModelSer
