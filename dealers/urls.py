from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DealerViewSet, CommissionViewSet, ProjectViewSet, ProjectCommissionViewSet

router = DefaultRouter()
router.register(r'dealers', DealerViewSet, basename='dealer')
router.register(r'commissions', CommissionViewSet, basename='commission')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-commissions', ProjectCommissionViewSet, basename='project-commission')

urlpatterns = [
    path('', include(router.urls)),
]
