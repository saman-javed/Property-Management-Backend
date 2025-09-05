from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TownViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r'towns', TownViewSet, basename='town')
router.register(r'town-projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
