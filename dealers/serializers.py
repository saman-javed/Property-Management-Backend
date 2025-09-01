from rest_framework import serializers
from .models import Dealer, Commission, ProjectCommission, Project
from decimal import Decimal

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']


class ProjectCommissionSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ProjectCommission
        fields = ['id', 'dealer', 'project', 'project_name', 'percent']
        extra_kwargs = {'dealer': {'required': False}}


class DealerSerializer(serializers.ModelSerializer):
    total_commission_paid = serializers.SerializerMethodField()
    commission_payable = serializers.SerializerMethodField()
    project_commissions = ProjectCommissionSerializer(many=True, read_only=False, required=False)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Dealer
        fields = ['id', 'name', 'phone', 'cnic', 'email', 'address',
                  'commission_rate', 'active', 'created_at',
                  'total_commission_paid', 'commission_payable', 'project_commissions']

    def get_total_commission_paid(self, obj):
        return obj.total_commission_paid()

    def get_commission_payable(self, obj):
        return obj.commission_payable()

    def validate_cnic(self, value):
        if value and (len(value) != 13 or not value.isdigit()):
            raise serializers.ValidationError("CNIC must be 13 digits")
        return value

    def create(self, validated_data):
        pcs = validated_data.pop('project_commissions', [])
        dealer = Dealer.objects.create(**validated_data)
        for pc in pcs:
            ProjectCommission.objects.create(dealer=dealer, **pc)
        return dealer

    def update(self, instance, validated_data):
        pcs = validated_data.pop('project_commissions', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        if pcs is not None:
            instance.project_commissions.all().delete()
            for pc in pcs:
                ProjectCommission.objects.create(dealer=instance, **pc)
        return instance


class CommissionSerializer(serializers.ModelSerializer):
    dealer_name = serializers.CharField(source='dealer.name', read_only=True)

    class Meta:
        model = Commission
        fields = ['id', 'dealer', 'dealer_name', 'amount', 'date',
                  'payment_method', 'reference_no', 'notes', 'voucher_no']

    def validate(self, data):
        dealer = data.get('dealer') or getattr(self.instance, 'dealer', None)
        amount = data.get('amount') or getattr(self.instance, 'amount', None)

        if dealer and amount:
            payable = dealer.commission_payable(up_to_date=data.get('date'))
            if Decimal(amount) > payable:
                raise serializers.ValidationError("Payment exceeds commission payable!")
        return data
