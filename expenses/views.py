from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import csv
from django.db.models import Sum
from .models import Expense, ExpenseCategory
from .serializers import ExpenseSerializer, ExpenseCategorySerializer


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all().order_by("name")
    serializer_class = ExpenseCategorySerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by("-date")
    serializer_class = ExpenseSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["note", "voucher_no"]
    ordering_fields = ["date", "amount"]

    def get_queryset(self):
        queryset = Expense.objects.all()
        town = self.request.query_params.get("town")
        project = self.request.query_params.get("project")
        office = self.request.query_params.get("office")
        date = self.request.query_params.get("date")

        if town:
            queryset = queryset.filter(town_id=town)
        if project:
            queryset = queryset.filter(project_id=project)
        if office:
            queryset = queryset.filter(office_id=office)
        if date:
            queryset = queryset.filter(date=date)

        return queryset
    



    # ✅ Custom action for Office Expense Report
    @action(detail=False, methods=["get"])
    def office_report(self, request):
        office_id = request.query_params.get("office")
        from_date = request.query_params.get("from")
        to_date = request.query_params.get("to")

        queryset = Expense.objects.all()
        if office_id:
            queryset = queryset.filter(office_id=office_id)
        if from_date and to_date:
            queryset = queryset.filter(date__range=[from_date, to_date])

        # group by category and sum amounts
        report = (
            queryset.values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("category__name")
        )

        total_amount = queryset.aggregate(total=Sum("amount"))["total"] or 0

        return Response({
            "report": report,
            "grand_total": total_amount,
        })





    @action(detail=False, methods=["get"])
    def export(self, request):
        queryset = self.get_queryset()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="expenses.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Voucher No", "Town", "Project", "Office", "Category", "Amount",
            "Date", "Payment Mode", "Reference", "Note"
        ])
        for exp in queryset:
            writer.writerow([
                exp.voucher_no,
                exp.town.name if exp.town else "",
                exp.project.name if exp.project else "",
                exp.office.name if exp.office else "",
                exp.category.name,
                exp.amount,
                exp.date,
                exp.payment_mode,
                exp.reference or "",
                exp.note or "",
            ])
        return response
