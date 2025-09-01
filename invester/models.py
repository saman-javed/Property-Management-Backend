from decimal import Decimal
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from towns_projects.models import Project


# CNIC format validator: 12345-1234567-1
cnic_validator = RegexValidator(
    regex=r'^\d{5}-\d{7}-\d{1}$',
    message="CNIC must be in the format 12345-1234567-1"
)


class Investor(models.Model):
    name = models.CharField(max_length=200)
    cnic = models.CharField(max_length=20, unique=True,null=True)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class InvestorProject(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name='investments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='investors')
    investment_amount = models.DecimalField(max_digits=18, decimal_places=2)
    profit_percent = models.DecimalField(max_digits=6, decimal_places=2)  # up to 100.00
    start_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('investor', 'project')

    def __str__(self):
        return f"{self.investor} - {self.project}"

    def clean(self):
        # Prevent aggregate > 100% for this project across investors
        from django.db.models import Sum
        qs = InvestorProject.objects.filter(project=self.project).exclude(pk=self.pk)
        total = qs.aggregate(sum=Sum('profit_percent'))['sum'] or Decimal('0')
        if (total + (self.profit_percent or Decimal('0'))) > Decimal('100'):
            raise ValidationError("Total profit percent allocation for this project would exceed 100%.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def total_project_profit(self):
        """
        Use Project.dynamic_net_profit instead of static net_profit
        """
        profit = getattr(self.project, 'dynamic_net_profit', None)
        if profit is None:
            return Decimal('0')
        return (Decimal(profit) * (Decimal(self.profit_percent) / Decimal('100')))

    def total_payouts(self):
        total = self.payouts.aggregate(s=models.Sum('amount'))['s'] or Decimal('0')
        return total

    def payable_balance(self):
        """
        Payable = Project Net Profit × Investor % − previous payouts.
        """
        total_profit = self.total_project_profit()
        paid = self.total_payouts()
        return (total_profit - paid)


class InvestorPayout(models.Model):
    investor_project = models.ForeignKey(InvestorProject, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    payout_date = models.DateField()
    mode = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'cash', 'bank'
    reference = models.CharField(max_length=200, blank=True, null=True)
    voucher_no = models.CharField(max_length=40, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Reference required for non-cash modes
        if self.mode and self.mode.lower() != 'cash' and not self.reference:
            raise ValidationError("Reference is required for non-cash payouts.")

        # Do not allow payout more than payable balance
        payable = self.investor_project.payable_balance()
        if Decimal(self.amount) > payable:
            raise ValidationError(f"Payout amount exceeds payable balance ({payable}).")

    def generate_voucher_no(self):
        # Simple voucher generation: INV-VCHR-<zero-padded count>
        count = InvestorPayout.objects.count() + 1
        return f"INV-VCHR-{count:06d}"

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.voucher_no:
            with transaction.atomic():
                self.voucher_no = self.generate_voucher_no()
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.investor_project} - {self.amount}"




