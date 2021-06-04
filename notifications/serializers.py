from rest_framework import serializers

from . import models


class ItemsSer(serializers.ModelSerializer):
    class Meta:
        model = models.Notifications
        fields = '__all__'
