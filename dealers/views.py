from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.http import HttpResponse
import csv
from datetime import datetime
from decimal import Decimal

from .models import Dealer, Commission, Project, ProjectCommission
from .serializers import DealerSerializer, CommissionSerializer, ProjectSerializer, ProjectCommissionSerializer
from buyers.models import Buyer

class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

    def list(self, request, *args, **kwargs):
        queryset = Dealer.objects.filter(active=True)
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(phone__icontains=search) |
                Q(cnic__icontains=search)
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        dealer = self.get_object()
        dealer.active = False
        dealer.save()
        return Response({"status": "Dealer deactivated"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def hard_delete(self, request, pk=None):
        """
        Permanently delete dealer from DB
        Usage: DELETE /api/dealers/{id}/hard_delete/
        """
        dealer = self.get_object()
        dealer.delete()
        return Response({"status": "Dealer permanently deleted"}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def payable(self, request, pk=None):
        dealer = self.get_object()
        up_to = request.query_params.get('up_to')
        up_to_date = None
        if up_to:
            try:
                up_to_date = datetime.strptime(up_to, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "dealer_id": dealer.id,
            "dealer_name": dealer.name,
            "total_eligible": dealer.commission_payable(up_to_date) + dealer.total_commission_paid(),
            "total_paid": dealer.total_commission_paid(),
            "payable": dealer.commission_payable(up_to_date)
        })


class CommissionViewSet(viewsets.ModelViewSet):
    queryset = Commission.objects.all().order_by('-date')
    serializer_class = CommissionSerializer

    @action(detail=False, methods=['get'])
    def dealer_ledger(self, request):
        dealer_id = request.query_params.get('dealer')
        if not dealer_id:
            return Response({"error": "Dealer ID required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            dealer = Dealer.objects.get(id=dealer_id)
        except Dealer.DoesNotExist:
            return Response({"error": "Dealer not found"}, status=status.HTTP_404_NOT_FOUND)

        date_from = request.query_params.get('from')
        date_to = request.query_params.get('to')
        export = request.query_params.get('export')

        buyers = dealer.buyers.all()
        if date_from:
            df = datetime.strptime(date_from, '%Y-%m-%d').date()
            buyers = buyers.filter(created_at__gte=df)
        if date_to:
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            buyers = buyers.filter(created_at__lte=dt)

        ledger = []
        balance = Decimal('0.00')
        for b in buyers:
            project_override = dealer.project_commissions.filter(project__name=b.property).first()
            percent = project_override.percent if project_override else dealer.commission_rate
            commission_amount = b.total_price * (percent / Decimal('100'))
            balance += commission_amount
            ledger.append({
                "date": b.created_at.date(),
                "description": f"Commission Accrued for {b.name}",
                "debit": 0,
                "credit": float(commission_amount),
                "balance": float(balance)
            })

        payments = dealer.commissions.order_by('date')
        if date_from:
            payments = payments.filter(date__gte=date_from)
        if date_to:
            payments = payments.filter(date__lte=date_to)

        for p in payments:
            balance -= p.amount
            ledger.append({
                "date": p.date,
                "description": f"Commission Paid - {p.voucher_no}",
                "debit": float(p.amount),
                "credit": 0,
                "balance": float(balance)
            })

        ledger_sorted = sorted(ledger, key=lambda x: x['date'])

        if export and export.lower() == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="ledger_{dealer_id}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Date', 'Description', 'Debit', 'Credit', 'Balance'])
            for row in ledger_sorted:
                writer.writerow([row['date'], row['description'], row['debit'], row['credit'], row['balance']])
            return response

        return Response({"ledger": ledger_sorted, "current_balance": float(balance)})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectCommissionViewSet(viewsets.ModelViewSet):
    queryset = ProjectCommission.objects.all()
    serializer_class = ProjectCommissionSerializer
