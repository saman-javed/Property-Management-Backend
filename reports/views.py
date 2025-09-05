from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from buyers.models import Installment, Buyer

class BuyerLedgerReportView(APIView):
    """
    Buyer Ledger Report API
    Filters: buyerId, from, to
    Returns: date, description, debit, credit
    """

    def get(self, request):
        buyer_id = request.GET.get('buyerId')
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')

        installments = Installment.objects.all().order_by('date')

        # Log the filtering criteria for debugging
        print(f"Filtering for buyerId: {buyer_id}, from: {from_date}, to: {to_date}")

        # Filter by buyer
        if buyer_id:
            installments = installments.filter(buyer_id=buyer_id)

        # Filter by dates
        if from_date:
            try:
                installments = installments.filter(date__gte=datetime.fromisoformat(from_date))
            except Exception as e:
                print("Invalid from_date:", e)
        if to_date:
            try:
                # Include the entire day for "to" date
                to_dt = datetime.fromisoformat(to_date) + timedelta(days=1)
                installments = installments.filter(date__lt=to_dt)
            except Exception as e:
                print("Invalid to_date:", e)

        # Log the number of installments found after filtering
        print(f"Found {installments.count()} installments after filtering.")

        # Build rows for the report
        rows = []
        for inst in installments:
            rows.append({
                "date": inst.date.strftime('%Y-%m-%d'),
                "description": "Installment Received",
                "debit": 0,
                "credit": float(inst.amount)
            })
            if inst.remarks:
                rows.append({
                    "date": inst.date.strftime('%Y-%m-%d'),
                    "description": inst.remarks,
                    "debit": float(inst.amount) if "late" in inst.remarks.lower() else 0,
                    "credit": 0
                })

        # Calculate the total balance
        total_credit = sum(r['credit'] for r in rows)
        total_debit = sum(r['debit'] for r in rows)
        balance = total_credit - total_debit

        # Return the response with the report data
        return Response({
            "rows": rows,
            "balance": balance
        }, status=status.HTTP_200_OK)












from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from buyers.models import Installment

class MonthlyInstallmentsReportView(APIView):
    """
    Returns all installments for a specific month/year.
    Optional filter: town name
    """

    def get(self, request):
        month = request.GET.get('month')
        year = request.GET.get('year')
        town = request.GET.get('townId')  # optional

        if not month or not year:
            return Response({"error": "Month and year are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response({"error": "Month and year must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter installments by month and year
        installments = Installment.objects.filter(date__year=year, date__month=month).order_by('date')

        # Optional: filter by town
        if town:
            installments = installments.filter(buyer__town__icontains=town)

        # Prepare response
        rows = []
        for inst in installments:
            rows.append({
                "buyer": inst.buyer.name,
                "dueDate": inst.date.strftime('%Y-%m-%d'),
                "amount": float(inst.amount),
                "status": inst.status
            })

        return Response(rows, status=status.HTTP_200_OK)








from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from decimal import Decimal
from dealers.models import Dealer

class DealerCommissionReportView(APIView):
    """
    Dealer Commission Report API
    Filters: dealer (optional), from, to
    Returns: ledger list
    """

    def get(self, request):
        dealer_id = request.GET.get('dealer')
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')

        if not from_date or not to_date:
            return Response({"error": "From and To dates are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            from_dt = datetime.fromisoformat(from_date)
            to_dt = datetime.fromisoformat(to_date)
        except Exception as e:
            return Response({"error": f"Invalid date format: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        if dealer_id:
            dealers = Dealer.objects.filter(id=dealer_id, active=True)
            if not dealers.exists():
                return Response({"error": "Dealer not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            dealers = Dealer.objects.filter(active=True)

        ledger = []

        for dealer in dealers:
            # Commission from buyers
            if hasattr(dealer, 'buyers'):
                buyers = dealer.buyers.filter(created_at__gte=from_dt, created_at__lte=to_dt)
                for b in buyers:
                    # Commission calculation
                    project_override = dealer.project_commissions.filter(project__name=b.property).first()
                    percent = project_override.percent if project_override else dealer.commission_rate
                    commission_amount = (b.total_price * percent / Decimal('100')).quantize(Decimal('0.01'))

                    ledger.append({
                        "date": b.created_at.strftime('%Y-%m-%d'),
                        "dealer": dealer.name,
                        "phone": dealer.phone,
                        "commission": float(commission_amount),
                        "description": f"Commission Accrued for {b.name}"
                    })

            # Commission payments
            if hasattr(dealer, 'commissions'):
                payments = dealer.commissions.filter(date__gte=from_dt, date__lte=to_dt)
                for p in payments:
                    ledger.append({
                        "date": p.date.strftime('%Y-%m-%d'),
                        "dealer": dealer.name,
                        "phone": dealer.phone,
                        "commission": float(-p.amount),  # negative for payment
                        "description": f"Commission Paid - {p.voucher_no}"
                    })

        # Sort by date
        ledger.sort(key=lambda x: x['date'])

        return Response({"ledger": ledger}, status=status.HTTP_200_OK)






# reports/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from invester.models import InvestorProject

class InvestorProfitReportView(APIView):
    """
    Investor Profit Report API
    Filters: investorId (optional), from (optional), to (optional)
    Returns: list of profits for each investor
    """

    def get(self, request):
        investor_id = request.GET.get('investorId')
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')

        qs = InvestorProject.objects.select_related('investor', 'project').all()

        # Filter by investor if provided
        if investor_id:
            qs = qs.filter(investor_id=investor_id)

        # Filter by from/to dates if provided
        if from_date:
            try:
                from_dt = datetime.fromisoformat(from_date)
                qs = qs.filter(start_date__gte=from_dt)
            except Exception as e:
                return Response({"error": f"Invalid from date: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        if to_date:
            try:
                to_dt = datetime.fromisoformat(to_date) + timedelta(days=1)
                qs = qs.filter(start_date__lt=to_dt)
            except Exception as e:
                return Response({"error": f"Invalid to date: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # Combine both filters properly
        report = []
        for ip in qs:
            # Only include if investor filter matches (should be already handled)
            report.append({
                "investor": ip.investor.name,
                "profit": float(ip.total_project_profit()),
                "date": ip.start_date.strftime('%Y-%m-%d') if ip.start_date else ''
            })

        return Response(report, status=status.HTTP_200_OK)















# reports/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from employees.models import SalaryPayment

class EmployeeSalaryReportView(APIView):
    """
    Employee Salary Report API
    Filters:
      - employeeId (optional)
      - employeeName (optional)
      - from (optional)
      - to (optional)
    """

    def get(self, request):
        employee_id = request.GET.get('employeeId')
        employee_name = request.GET.get('employeeName')
        from_date = request.GET.get('from')
        to_date = request.GET.get('to')

        qs = SalaryPayment.objects.select_related('employee').all().order_by('pay_date')

        # ✅ Filter by employeeId
        if employee_id:
            qs = qs.filter(employee_id=employee_id)

        # ✅ Filter by employeeName (case-insensitive match)
        if employee_name:
            qs = qs.filter(employee__name__icontains=employee_name)

        # ✅ Filter by date range
        if from_date:
            try:
                from_dt = datetime.fromisoformat(from_date)
                qs = qs.filter(pay_date__gte=from_dt)
            except Exception as e:
                return Response({"error": f"Invalid from date: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        if to_date:
            try:
                to_dt = datetime.fromisoformat(to_date) + timedelta(days=1)
                qs = qs.filter(pay_date__lt=to_dt)
            except Exception as e:
                return Response({"error": f"Invalid to date: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Build the report
        report = []
        for sp in qs:
            report.append({
                "employee": sp.employee.name,
                "salary": float(sp.amount),
                "date": sp.pay_date.strftime('%Y-%m-%d'),
                "month": sp.month,
                "voucher_no": sp.voucher_no,
                "mode": sp.mode,
                "reference": sp.reference,
            })

        return Response(report, status=status.HTTP_200_OK)
# reports/views.py
from employees.models import Employee
from rest_framework.views import APIView
from rest_framework.response import Response

class EmployeeListView(APIView):
    """Return list of all employees (id + name)"""

    def get(self, request):
        employees = Employee.objects.all().order_by('name')
        data = [{"id": e.id, "name": e.name} for e in employees]
        return Response(data)




















from decimal import Decimal
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from buyers.models import Buyer, Installment
from dealers.models import ProjectCommission
from expenses.models import Expense
from .serializers import ProfitLossSerializer

@api_view(['GET'])
def town_profit_loss(request, town_name):
    # --- Revenue (advance + installments) ---
    buyers = Buyer.objects.filter(town=town_name)
    total_advance = buyers.aggregate(total=Sum("advance"))["total"] or Decimal("0.00")
    total_installments = Installment.objects.filter(buyer__in=buyers).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    revenue = total_advance + total_installments

    # --- Dealer Commission ---
    dealer_commission = Decimal("0.00")
    for buyer in buyers:
        project_override = ProjectCommission.objects.filter(
            dealer=buyer.dealer, project__name=buyer.property
        ).first()
        percent = project_override.percent if project_override else buyer.dealer.commission_rate
        dealer_commission += (buyer.total_price * percent / Decimal("100")).quantize(Decimal("0.01"))

    # --- Expenses ---
    expenses = Expense.objects.filter(town__id=town_name).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    # --- Net Profit ---
    net_profit = revenue - (dealer_commission + expenses)

    data = {
        "town": town_name,
        "total_revenue": revenue,
        "total_dealer_commission": dealer_commission,
        "total_expenses": expenses,
        "net_profit_loss": net_profit,
    }
    return Response(ProfitLossSerializer(data).data)

















from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from buyers.models import Buyer, Installment
from expenses.models import Expense
from decimal import Decimal

@api_view(['GET'])
def overall_profit_loss(request):
    # --- Income ---
    cash_income = (
        Buyer.objects.filter(sale_type="Cash")
        .aggregate(total=Sum("total_price"))["total"] or Decimal("0.00")
    )

    advance_income = (
        Buyer.objects.filter(sale_type="Installment")
        .aggregate(total=Sum("advance"))["total"] or Decimal("0.00")
    )

    installment_income = (
        Installment.objects.filter(status="Paid")
        .aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    )

    total_income = cash_income + advance_income + installment_income

    # --- Expenses ---
    total_expense = Expense.objects.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

    # --- Profit/Loss ---
    profit_loss = total_income - total_expense

    return Response({
        "income": {
            "cash_sales": cash_income,
            "advances": advance_income,
            "installments": installment_income,
            "total_income": total_income,
        },
        "expenses": {
            "total_expense": total_expense,
        },
        "profit_loss": profit_loss,
    })
























