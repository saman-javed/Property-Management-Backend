from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import csv

from .models import Office
from .serializers import OfficeSerializer

class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all().order_by('-created_at')
    serializer_class = OfficeSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.GET.get('q', '')
        offices = self.queryset.filter(office_name__icontains=q) | self.queryset.filter(location__icontains=q)
        serializer = self.get_serializer(offices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="offices.csv"'
        writer = csv.writer(response)
        writer.writerow(['Office Name', 'Location', 'Phone', 'Manager', 'Active'])
        for o in self.queryset:
            writer.writerow([o.office_name, o.location, o.phone, o.manager, o.active])
        return response
