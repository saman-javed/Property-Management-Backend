from rest_framework import serializers
from .models import Office

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ['id', 'office_name', 'location', 'phone', 'manager', 'active']
