from django.contrib import admin
from django.urls import path
from property.location_view import LocationView
from property.views import PropertyView  # <-- Correct import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/properties/', PropertyView.as_view(), name='property-list'),
    path('api/property/<int:pk>/', PropertyView.as_view(), name='Property-detail'),

    path('api/locations/', LocationView.as_view(), name='locations-list'),
    path('api/location/<int:pk>/', LocationView.as_view(), name='location-detail'),
]