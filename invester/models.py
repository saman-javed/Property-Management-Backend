from django.db import models

# Create your models here.
from decimal import Decimal
from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

# Import your Project model (adjust path if needed)
from towns_projects.models import Project

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
        Assumes Project model has a numeric field `net_profit` (Decimal).
        If not present, returns 0.0 — you should wire project net profit from accounting.
        """
        net_profit = getattr(self.project, 'net_profit', None)
        if net_profit is None:
            return Decimal('0')
        return (Decimal(net_profit) * (Decimal(self.profit_percent) / Decimal('100')))

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
        # reference required for non-cash modes
        if self.mode and self.mode.lower() != 'cash' and not self.reference:
            raise ValidationError("Reference is required for non-cash payouts.")

        # Do not allow payout more than payable balance
        payable = self.investor_project.payable_balance()
        if Decimal(self.amount) > payable:
            raise ValidationError(f"Payout amount exceeds payable balance ({payable}).")

    def generate_voucher_no(self):
        # Simple voucher generation: INV-VCHR-<zero-padded count>
        # NOTE: For heavy concurrent systems, use a DB sequence or separate table to avoid race conditions.
        count = InvestorPayout.objects.count() + 1
        return f"INV-VCHR-{count:06d}"

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.voucher_no:
            # ensure atomic-ish generation (not perfect race-proof)
            with transaction.atomic():
                # pick next voucher
                self.voucher_no = self.generate_voucher_no()
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.investor_project} - {self.amount}"
