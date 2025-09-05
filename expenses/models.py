from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError

# Import existing models
from towns_projects.models import Town, Project
from offices.models import Office


class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    town = models.ForeignKey(Town, null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    office = models.ForeignKey(Office, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.PROTECT)

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()

    PAYMENT_MODES = [
        ("cash", "Cash"),
        ("bank", "Bank"),
        ("cheque", "Cheque"),
        ("online", "Online"),
    ]
    payment_mode = models.CharField(max_length=10, choices=PAYMENT_MODES)
    reference = models.CharField(max_length=100, null=True, blank=True)

    note = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to="expense_attachments/", blank=True, null=True)

    voucher_no = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.voucher_no:
            last_id = Expense.objects.count() + 1
            self.voucher_no = f"V{last_id:05d}"
        super().save(*args, **kwargs)

    def clean(self):
        if not (self.town or self.project or self.office):
            raise ValidationError("Either Town/Project or Office is required.")
        if self.payment_mode != "cash" and not self.reference:
            raise ValidationError("Reference is required for non-cash payments.")

    def __str__(self):
        return f"{self.voucher_no} - {self.amount}"
