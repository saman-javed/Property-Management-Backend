from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmployeeViewSet, SalaryPaymentViewSet

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'salaries', SalaryPaymentViewSet, basename='salary')

urlpatterns = [
    path('', include(router.urls)),
]
