from rest_framework import viewsets
from .models import PropertyAmenity
from .serializers import PropertyAmenitySerializer

class PropertyAmenityViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing PropertyAmenity instances.
    """
    queryset = PropertyAmenity.objects.all()
    serializer_class = PropertyAmenitySerializer
