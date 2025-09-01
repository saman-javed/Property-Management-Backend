# towns_projects/models.py
from django.db import models
from django.db.models import Sum
from decimal import Decimal, ROUND_HALF_UP

class Town(models.Model):
    name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    total_plots = models.PositiveIntegerField()
    map_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    # keep offices ManyToMany - adjust import path in real project
    offices = models.ManyToManyField('offices.Office', related_name='towns', blank=True)

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

    # authoritative net profit stored on Project
    net_profit = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal('0.00'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

    @property
    def dynamic_net_profit(self):
        """
        Example fallback calculation: 10% of total invested amount for the project.
        Use this if you want an auto-calculated value for demo/testing.
        In production, prefer setting net_profit manually (accounting).
        """
        agg = self.investors.aggregate(total=Sum('investment_amount'))
        total_invested = agg['total'] or Decimal('0')
        profit = (Decimal(total_invested) * Decimal('0.10')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return profit
