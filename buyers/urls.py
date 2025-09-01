# buyers/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BuyerViewSet, InstallmentViewSet

router = DefaultRouter()
router.register(r'buyers', BuyerViewSet)
router.register(r'installments', InstallmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
