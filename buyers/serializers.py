# buyers/serializers.py
from rest_framework import serializers
from .models import Buyer, Installment

class BuyerSerializer(serializers.ModelSerializer):
    dealer_name = serializers.CharField(source='dealer.name', read_only=True)  # display dealer name

    class Meta:
        model = Buyer
        fields = '__all__'


class InstallmentSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.name', read_only=True)

    class Meta:
        model = Installment
        fields = '__all__'
