# investors/serializers.py
from rest_framework import serializers
from .models import Investor, InvestorProject, InvestorPayout
from decimal import Decimal

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['id', 'name', 'cnic', 'email', 'contact', 'address', 'start_date', 'created_at', 'updated_at']


class InvestorProjectSerializer(serializers.ModelSerializer):
    investor_name = serializers.CharField(source='investor.name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    payable_balance = serializers.SerializerMethodField()

    class Meta:
        model = InvestorProject
        fields = ['id', 'investor', 'investor_name', 'project', 'project_name',
                  'investment_amount', 'profit_percent', 'start_date', 'payable_balance']

    def get_payable_balance(self, obj):
        # return as numeric value (float) so Angular receives a number
        return float(obj.payable_balance())


class InvestorProjectQuickEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProject
        fields = ['id', 'investor', 'project', 'profit_percent']

    def validate(self, data):
        instance = self.instance
        profit_percent = data.get('profit_percent', instance.profit_percent if instance else 0)

        from django.db.models import Sum
        qs = InvestorProject.objects.filter(project=instance.project).exclude(pk=instance.pk)
        total = qs.aggregate(sum=Sum('profit_percent'))['sum'] or Decimal('0')

        if Decimal(total) + Decimal(profit_percent) > Decimal('100'):
            raise serializers.ValidationError({
                "profit_percent": "Total profit percent allocation for this project would exceed 100%."
            })
        return data


class InvestorPayoutSerializer(serializers.ModelSerializer):
    investor_name = serializers.CharField(source='investor_project.investor.name', read_only=True)
    project_name = serializers.CharField(source='investor_project.project.name', read_only=True)
    voucher_no = serializers.CharField(read_only=True)

    class Meta:
        model = InvestorPayout
        fields = ['id', 'investor_project', 'investor_name', 'project_name',
                  'amount', 'payout_date', 'mode', 'reference', 'voucher_no', 'created_at']

    def validate(self, data):
        investor_project = data.get('investor_project')
        amount = data.get('amount')
        mode = data.get('mode', '').lower()
        reference = data.get('reference')

        if investor_project:
            payable = investor_project.payable_balance()
            if Decimal(amount) > payable:
                raise serializers.ValidationError({
                    "amount": f"Payout amount exceeds payable balance ({payable})."
                })

        if mode and mode != 'cash' and not reference:
            raise serializers.ValidationError({
                "reference": "Reference is required for non-cash payouts."
            })

        return data
