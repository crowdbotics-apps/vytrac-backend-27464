from Functions.DynamicSer import DynamicSerializer
from Functions.MyViews import ItemView, ItemsView
from .. import models

MyModel = models.Profile


class ModelSer(DynamicSerializer):
    # dates = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = MyModel
        fields = '__all__'
        # fields = [*[x.name for x in MyModel._meta.fields], 'dates']


class Views(ItemsView):
    queryset = MyModel.objects.all()
    serializer_class = ModelSer


class View(ItemView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ModelSer
