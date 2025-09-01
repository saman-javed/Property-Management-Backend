from django.shortcuts import render

# Create your views here.
# buyers/views.py
from rest_framework import viewsets
from .models import Buyer, Installment
from .serializers import BuyerSerializer, InstallmentSerializer
from .installment_service import generate_installment_schedule  # helper function
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# -------------------------
# Buyer ViewSet
# -------------------------
class BuyerViewSet(viewsets.ModelViewSet):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

    def perform_create(self, serializer):
        buyer = serializer.save()
        # Auto-generate installment schedule if sale_type is Installment
        if buyer.sale_type == "Installment":
            generate_installment_schedule(buyer)

    def perform_update(self, serializer):
        buyer = serializer.save()
        # Regenerate installments if sale_type is Installment
        if buyer.sale_type == "Installment":
            generate_installment_schedule(buyer)


# -------------------------
# Installment ViewSet
# -------------------------
class InstallmentViewSet(viewsets.ModelViewSet):
    queryset = Installment.objects.all().order_by('-date')
    serializer_class = InstallmentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['buyer', 'status', 'date']  # Filters for buyer, status, date
    ordering_fields = ['date', 'amount']
