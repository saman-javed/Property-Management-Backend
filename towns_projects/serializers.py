# towns_projects/serializers.py
from rest_framework import serializers
from .models import Town, Project
# from offices.serializers import OfficeSerializer  # adjust import as needed

class TownSerializer(serializers.ModelSerializer):
    # If you have OfficeSerializer, uncomment and use offices_detail
    # offices_detail = OfficeSerializer(source='offices', many=True, read_only=True)

    class Meta:
        model = Town
        fields = ['id', 'name', 'city', 'total_plots', 'map_url', 'description', 'active', 'offices']  # add offices_detail if needed


class ProjectSerializer(serializers.ModelSerializer):
    dynamic_net_profit = serializers.DecimalField(max_digits=18, decimal_places=2, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'city', 'total_plots', 'map_url',
            'description', 'active', 'town', 'net_profit', 'dynamic_net_profit'
        ]
