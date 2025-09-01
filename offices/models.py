from django.db import models

# Create your models here.
from django.db import models

class Office(models.Model):
    office_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, blank=True, null=True)
    manager = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)  # Optional if you want to filter active/inactive

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.office_name
