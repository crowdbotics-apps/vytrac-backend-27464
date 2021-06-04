from Functions.DynamicSer import DynamicSerializer
from Functions.MyViews import ItemView, ItemsView
from .. import models as MD

MyModel = MD.Profile


# class Album(models.Model):
#     album_name = models.ManyToManyField(max_length=100)
#     artist = models.CharField(max_length=100)


# class Track(models.Model):
#     album = models.Man(
#         Album, related_name='tracks', on_delete=models.CASCADE)
#     order = models.IntegerField()
#     title = models.CharField(max_length=100)
#     duration = models.IntegerField()

#     class Meta:
#         unique_together = ['album', 'order']
#         ordering = ['order']

#     def __str__(self):
#         return '%d: %s' % (self.order, self.title)


# class AlbumSerializer(serializers.ModelSerializer):
#     tracks = serializers.StringRelatedField(many=True)

#     class Meta:
#         model = Album
#         fields = ['album_name', 'artist', 'tracks']


# class MyViews(ItemsView):
#     queryset = Album.objects.all()
#     serializer_class = AlbumSerializer


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
