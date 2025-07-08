from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Location
from .serializers import LocationSerializer


class LocationView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                Location_obj = Location.objects.get(pk=pk)
            except Location.DoesNotExist:
                return Response({'error': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = LocationSerializer(Location_obj)
            return Response(serializer.data)
        else:
            Locations = Location.objects.all()
            serializer = LocationSerializer(Locations, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is not None:
            try:
                Location_obj = Location.objects.get(pk=pk)
            except Location.DoesNotExist:
                return Response({'error': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = LocationSerializer(Location_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Please provide a valid Location ID.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            try:
                Location_obj = Location.objects.get(pk=pk)
            except Location.DoesNotExist:
                return Response({'error': 'Location not found.'}, status=status.HTTP_404_NOT_FOUND)
            Location_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            Location.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
