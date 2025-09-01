from django.db import models
from django.core.validators import RegexValidator
from offices.models import Office  # Link to your Office app

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\d{10,15}$', 'Phone must be numeric (10-15 digits)')]
    )
    cnic = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(r'^\d{5}-\d{7}-\d$', 'Invalid CNIC format')]
    )
    designation = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    office = models.ForeignKey(Office, on_delete=models.PROTECT)  # Foreign key to Office
    joining_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SalaryPayment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    month = models.CharField(max_length=20)  # Or DateField if preferred
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pay_date = models.DateField()
    mode = models.CharField(max_length=50, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    voucher_no = models.CharField(max_length=20, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employee', 'month')  # Prevent duplicate month payments

    def save(self, *args, **kwargs):
        # Auto-generate voucher number
        if not self.voucher_no:
            last_id = SalaryPayment.objects.all().count() + 1
            self.voucher_no = f'VCHR-{last_id:05d}'

        # Validation: Mode & Reference required if non-cash
        if self.mode and self.mode.lower() != 'cash':
            if not self.reference:
                raise ValueError("Reference is required for non-cash payments")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name} - {self.month}"
