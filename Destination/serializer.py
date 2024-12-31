from rest_framework import serializers
from .models import DestinationModel
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationModel
        fields = "__all__"