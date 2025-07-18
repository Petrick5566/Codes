from django.contrib import admin
from django.urls import path
from property.views import RegisterView, CustomTokenObtainPairView
from property.location_view import LocationView
from property.views import PropertyView  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/properties/', PropertyView.as_view(), name='property-list'),
    path('api/property/<int:pk>/', PropertyView.as_view(), name='Property-detail'),

    path('api/locations/', LocationView.as_view(), name='locations-list'),
    path('api/location/<int:pk>/', LocationView.as_view(), name='location-detail'),

    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
]