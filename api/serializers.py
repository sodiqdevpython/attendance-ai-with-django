from rest_framework import serializers
from .models import Attendense


class AttendenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendense
        fields = ['id', 'user', 'direction', 'created']
