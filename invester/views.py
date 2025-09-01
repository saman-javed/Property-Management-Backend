from django.shortcuts import render
import csv
from decimal import Decimal
from django.http import HttpResponse
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Investor, InvestorProject, InvestorPayout
from .serializers import (
    InvestorSerializer,
    InvestorProjectSerializer,
    InvestorProjectQuickEditSerializer,
    InvestorPayoutSerializer
)


# ------------------- Investor ------------------- #
class InvestorViewSet(viewsets.ModelViewSet):
    queryset = Investor.objects.all().order_by('-created_at')
    serializer_class = InvestorSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.GET.get('q', '').strip()
        if not q:
            return Response(self.get_serializer(self.queryset, many=True).data)
        qs = self.queryset.filter(name__icontains=q) | self.queryset.filter(cnic__icontains=q)
        return Response(self.get_serializer(qs.distinct(), many=True).data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="investors.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Name', 'CNIC', 'Email', 'Contact', 'Address', 'Start Date', 'Created At'])
        for i in self.queryset:
            writer.writerow([i.id, i.name, i.cnic, i.email, i.contact, i.address, i.start_date, i.created_at])
        return response


# ------------------- InvestorProject ------------------- #
class InvestorProjectViewSet(viewsets.ModelViewSet):
    queryset = InvestorProject.objects.all().order_by('-id')
    serializer_class = InvestorProjectSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                instance = serializer.save()
                return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def quick_edit_profit(self, request, pk=None):
        ip = self.get_object()
        serializer = InvestorProjectQuickEditSerializer(ip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return Response(InvestorProjectSerializer(ip).data)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def export(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="investor_projects.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Investor', 'Project', 'Investment Amount', 'Profit %', 'Start Date', 'Payable Balance'])
        for ip in self.queryset:
            writer.writerow([
                ip.id,
                ip.investor.name,
                getattr(ip.project, 'name', ''),
                ip.investment_amount,
                ip.profit_percent,
                ip.start_date,
                ip.payable_balance()
            ])
        return response

    @action(detail=True, methods=['get'])
    def ledger(self, request, pk=None):
        ip = self.get_object()
        payouts_qs = ip.payouts.order_by('payout_date').values(
            'id', 'amount', 'payout_date', 'mode', 'reference', 'voucher_no'
        )
        total_profit = ip.total_project_profit()
        paid = ip.total_payouts()
        balance = ip.payable_balance()
        return Response({
            "investor": ip.investor.name,
            "project": getattr(ip.project, 'name', ''),
            "profit_percent": ip.profit_percent,
            "total_profit_share": total_profit,
            "total_paid": paid,
            "balance": balance,
            "payouts": list(payouts_qs)
        })


# ------------------- InvestorPayout ------------------- #
class InvestorPayoutViewSet(viewsets.ModelViewSet):
    queryset = InvestorPayout.objects.all().order_by('-payout_date')
    serializer_class = InvestorPayoutSerializer

    @action(detail=False, methods=['get'])
    def balance(self, request):
        ip_id = request.query_params.get('investor_project')
        if not ip_id:
            return Response({"detail": "Provide ?investor_project=<id> as query param."}, status=400)
        try:
            ip = InvestorProject.objects.get(pk=ip_id)
        except InvestorProject.DoesNotExist:
            return Response({"detail": "InvestorProject not found."}, status=404)
        # return numeric value (float) for frontend
        return Response({"payable_balance": float(ip.payable_balance())})