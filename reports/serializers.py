from rest_framework import serializers

class ProfitLossSerializer(serializers.Serializer):
    town = serializers.CharField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_dealer_commission = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_profit_loss = serializers.DecimalField(max_digits=12, decimal_places=2)
