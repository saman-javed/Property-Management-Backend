from rest_framework import serializers
from .models import Employee, SalaryPayment

class EmployeeSerializer(serializers.ModelSerializer):
    office_name = serializers.CharField(source='office.office_name', read_only=True)  # Added field

    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'phone', 'cnic', 'designation', 'salary',
            'office', 'office_name',  # office_name added
            'joining_date', 'is_active',
            'created_at', 'updated_at'
        ]


class SalaryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryPayment
        fields = [
            'id', 'employee', 'month', 'amount', 'pay_date', 'mode',
            'reference', 'voucher_no', 'created_at', 'updated_at'
        ]
