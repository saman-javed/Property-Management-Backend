# towns_projects/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import csv

from .models import Town, Project
from .serializers import TownSerializer, ProjectSerializer

class TownViewSet(viewsets.ModelViewSet):
    serializer_class = TownSerializer

    def get_queryset(self):
        return Town.objects.all().order_by('-created_at')

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.GET.get('q', '')
        qs = self.get_queryset().filter(name__icontains=q) | self.get_queryset().filter(city__icontains=q)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="towns.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'City', 'Total Plots', 'Map URL', 'Description', 'Active', 'Offices'])
        for t in self.get_queryset():
            offices_names = ", ".join([str(o) for o in t.offices.all()])
            writer.writerow([t.name, t.city, t.total_plots, t.map_url, t.description, t.active, offices_names])
        return response


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all().order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=400)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.GET.get('q', '')
        qs = self.get_queryset().filter(name__icontains=q) | self.get_queryset().filter(city__icontains=q)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="projects.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'City', 'Total Plots', 'Map URL', 'Description', 'Active', 'Town', 'Net Profit'])
        for p in self.get_queryset():
            town_name = p.town.name if p.town else ""
            writer.writerow([p.name, p.city, p.total_plots, p.map_url, p.description, p.active, town_name, p.net_profit])
        return response
