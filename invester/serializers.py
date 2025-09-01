from rest_framework import serializers
from .models import Investor, InvestorProject, InvestorPayout

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
        return obj.payable_balance()


class InvestorProjectQuickEditSerializer(serializers.ModelSerializer):
    """
    For quick edit of profit percent only.
    """
    class Meta:
        model = InvestorProject
        fields = ['id', 'investor', 'project', 'profit_percent']


class InvestorPayoutSerializer(serializers.ModelSerializer):
    investor_name = serializers.CharField(source='investor_project.investor.name', read_only=True)
    project_name = serializers.CharField(source='investor_project.project.name', read_only=True)
    voucher_no = serializers.CharField(read_only=True)

    class Meta:
        model = InvestorPayout
        fields = ['id', 'investor_project', 'investor_name', 'project_name',
                  'amount', 'payout_date', 'mode', 'reference', 'voucher_no', 'created_at']
