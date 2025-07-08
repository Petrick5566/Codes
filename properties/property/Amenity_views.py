from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Amenity
from .serializers import AmenitySerializer

class AmenityView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                amenity = Amenity.objects.get(pk=pk)
            except Amenity.DoesNotExist:
                return Response({'error': 'Amenity not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = AmenitySerializer(amenity)
            return Response(serializer.data)
        else:
            amenities = Amenity.objects.all()
            serializer = AmenitySerializer(amenities, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is not None:
            try:
                amenity = Amenity.objects.get(pk=pk)
            except Amenity.DoesNotExist:
                return Response({'error': 'Amenity not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = AmenitySerializer(amenity, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Please provide a valid Amenity ID.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            try:
                amenity = Amenity.objects.get(pk=pk)
            except Amenity.DoesNotExist:
                return Response({'error': 'Amenity not found.'}, status=status.HTTP_404_NOT_FOUND)
            amenity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            Amenity.objects.all().delete()
