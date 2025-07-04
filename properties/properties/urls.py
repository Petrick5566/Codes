from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/properties/', views.PropertyView, name='property-list'),
    path('api/property/<int:pk>/', views.PropertyView, name='Property-detail'),
]