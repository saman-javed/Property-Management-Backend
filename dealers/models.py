from django.db import models

# Create your models here.
from decimal import Decimal
from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db.models import Sum
from buyers.models import Buyer

phone_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message="Phone must be 10-15 digits and may start with +."
)

class Project(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Dealer(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15, unique=True, validators=[phone_validator])
    cnic = models.CharField(max_length=13, null=False, blank=False, unique=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('5.00'),
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_commission_paid(self):
        return self.commissions.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    def commission_payable(self, up_to_date=None):
        buyers = self.buyers.all()
        if up_to_date:
            buyers = buyers.filter(created_at__lte=up_to_date)

        total_eligible = Decimal('0.00')
        for b in buyers:
            project_override = ProjectCommission.objects.filter(dealer=self, project__name=b.property).first()
            percent = project_override.percent if project_override else self.commission_rate
            total_eligible += (b.total_price * percent / Decimal('100')).quantize(Decimal('0.01'))

        total_paid = self.total_commission_paid()
        payable = total_eligible - total_paid
        return payable if payable > 0 else Decimal('0.00')

    def __str__(self):
        return self.name


class ProjectCommission(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='project_commissions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    percent = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        unique_together = ('dealer', 'project')

    def __str__(self):
        return f"{self.dealer.name} - {self.project.name} : {self.percent}%"


class Commission(models.Model):
    PAYMENT_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
    ]

    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='commissions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES)
    reference_no = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    voucher_no = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.voucher_no:
            with transaction.atomic():
                last = Commission.objects.select_for_update().order_by('-id').first()
                next_no = last.id + 1 if last else 1
                self.voucher_no = f"VCH{next_no:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dealer.name} - {self.amount} - {self.voucher_no}"
