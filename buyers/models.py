from django.db import models

# Create your models here.
# buyers/models.py
from django.db import models

class Buyer(models.Model):
    SALE_TYPE_CHOICES = [
        ('Cash', 'Cash'),
        ('Installment', 'Installment'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=100)
    cnic = models.CharField(max_length=13, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    property = models.CharField(max_length=100, default='Unknown')
    sale_type = models.CharField(max_length=20, choices=SALE_TYPE_CHOICES, default='Installment')
    dealer = models.ForeignKey('dealers.Dealer', on_delete=models.CASCADE, related_name="buyers")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    advance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    installment_plan = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    address = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    fileNo = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.cnic}"



class Installment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    ]

    MODE_CHOICES = [
        ('Cash', 'Cash'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cheque', 'Cheque'),
    ]

    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='installments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default='Cash')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.buyer.name} - {self.amount} - {self.status}"
