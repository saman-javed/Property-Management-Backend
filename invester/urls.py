from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InvestorViewSet, InvestorProjectViewSet, InvestorPayoutViewSet

router = DefaultRouter()
router.register(r'investors', InvestorViewSet, basename='investor')
router.register(r'investor-projects', InvestorProjectViewSet, basename='investor-project')
router.register(r'investor-payouts', InvestorPayoutViewSet, basename='investor-payout')

urlpatterns = [
    path('', include(router.urls)),
]
