from django.db import models

# Create your models here.
from django.db import models
from offices.models import Office  # Link Towns to Office

class Town(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    total_plots = models.PositiveIntegerField()
    map_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    offices = models.ManyToManyField(Office, related_name='towns', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city})"


class Project(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    total_plots = models.PositiveIntegerField()
    map_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city})"
