from rest_framework import serializers
from .models import Town, Project
from offices.serializers import OfficeSerializer

class TownSerializer(serializers.ModelSerializer):
    offices_detail = OfficeSerializer(source='offices', many=True, read_only=True)

    class Meta:
        model = Town
        fields = ['id', 'name', 'city', 'total_plots', 'map_url', 'description', 'active', 'offices', 'offices_detail']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'city', 'total_plots', 'map_url', 'description', 'active','town' ]






