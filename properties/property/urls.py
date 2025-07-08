from rest_framework.routers import DefaultRouter
from .PropertyAmenity_views import PropertyAmenityViewSet

router = DefaultRouter()
router.register(r'propertyamenities', PropertyAmenityViewSet, basename='propertyamenity')

urlpatterns = router.urls
