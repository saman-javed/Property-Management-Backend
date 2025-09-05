from django.urls import path
from .views import (
    BuyerLedgerReportView,
    MonthlyInstallmentsReportView,
    DealerCommissionReportView,
    InvestorProfitReportView,
    EmployeeSalaryReportView,
    EmployeeListView,
    # OfficeExpenseReportView,
    town_profit_loss,
    overall_profit_loss,   # ✅ add this
)

urlpatterns = [
    path('buyer-ledger/', BuyerLedgerReportView.as_view(), name='buyer-ledger-report'),
    path('monthly-installments/', MonthlyInstallmentsReportView.as_view(), name='monthly-installments-report'),
    path('dealer-commission/', DealerCommissionReportView.as_view(), name='dealer-commission-report'),
    path('investor-profit/', InvestorProfitReportView.as_view(), name='investor-profit-report'),
    path('employee-salary/', EmployeeSalaryReportView.as_view(), name='employee-salary-report'), 
    path('employee-list/', EmployeeListView.as_view(), name='employee-list'),
    # path('office-expense/', OfficeExpenseReportView.as_view(), name='office-expense-report'),
    path("profit-loss/<str:town_name>/", town_profit_loss, name="town-profit-loss"),
    path("profit-loss/overall/", overall_profit_loss, name="overall-profit-loss"),  # ✅ new endpoint
]
