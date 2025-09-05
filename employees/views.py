from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
import csv

from .models import Employee, SalaryPayment
from .serializers import EmployeeSerializer, SalaryPaymentSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('-created_at')
    serializer_class = EmployeeSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.GET.get('q', '')
        employees = self.queryset.filter(name__icontains=q) | \
                    self.queryset.filter(cnic__icontains=q) | \
                    self.queryset.filter(phone__icontains=q)
        serializer = self.get_serializer(employees, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employees.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Phone', 'CNIC', 'Designation', 'Salary', 'Office', 'Joining Date', 'Active'])
        for e in self.queryset:
            writer.writerow([
                e.name, e.phone, e.cnic, e.designation, e.salary,
                e.office.office_name, e.joining_date, e.is_active
            ])
        return response


class SalaryPaymentViewSet(viewsets.ModelViewSet):
    queryset = SalaryPayment.objects.all().order_by('-pay_date')
    serializer_class = SalaryPaymentSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def ledger(self, request):
        employee_id = request.GET.get('employee')
        month = request.GET.get('month')
        salaries = self.queryset
        if employee_id:
            salaries = salaries.filter(employee_id=employee_id)
        if month:
            salaries = salaries.filter(month=month)
        serializer = self.get_serializer(salaries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="salary_ledger.csv"'
        writer = csv.writer(response)
        writer.writerow(['Employee', 'Month', 'Amount', 'Pay Date', 'Mode', 'Reference', 'Voucher No'])
        for s in self.queryset:
            writer.writerow([
                s.employee.name, s.month, s.amount, s.pay_date, s.mode, s.reference, s.voucher_no
            ])
        return response



