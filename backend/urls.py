from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('buyers.urls')),
    path('api/', include('dealers.urls')),
    path('api/', include('offices.urls')),   # <-- Add Offices
    path('api/', include('towns_projects.urls')),  
    path('api/', include('employees.urls')),  
    path('api/', include('invester.urls')),
]
