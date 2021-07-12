from rest_framework import serializers
from . import models


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Url
        fields = '__all__'
