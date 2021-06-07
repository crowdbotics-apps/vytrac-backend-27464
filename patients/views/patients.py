from rest_framework import status
from rest_framework.response import Response

from Functions.DynamicSer import DynamicSerializer
from Functions.MyViews import ItemView, ItemsView
from Functions.debuging import Debugging
from .. import models

MyModel = models.Patient


class ModelSer(DynamicSerializer):
    # dates = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = MyModel
        fields = '__all__'
        # fields = [*[x.name for x in MyModel._meta.fields], 'dates']


class Views(ItemsView):
    def post(self, request, format=None):
        if "{" in str(request.data['symptoms']):
            symptoms_ids = []
            symptoms = request.data['symptoms']
            for s in symptoms:
                pass
                try:
                  models.Symptom.objects.get(name=s['name'])
                except:
                    models.Symptom.objects.create(name=s['name'])
                id = models.Symptom.objects.get(name=s['name']).id
                symptoms_ids.append(id)
            request.data['symptoms'] = symptoms_ids

        serializer = self.serializer_class(
            data=request.data, context={'method': 'add', 'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    queryset = MyModel.objects.all()
    serializer_class = ModelSer


class View(ItemView):
    MyModel = MyModel
    queryset = MyModel.objects.all()
    serializer_class = ModelSer
