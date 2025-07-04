from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer


class PropertyView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            try:
                property_obj = Property.objects.get(pk=pk)
            except Property.DoesNotExist:
                return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PropertySerializer(property_obj)
            return Response(serializer.data)
        else:
            properties = Property.objects.all()
            serializer = PropertySerializer(properties, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is not None:
            try:
                property_obj = Property.objects.get(pk=pk)
            except Property.DoesNotExist:
                return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PropertySerializer(property_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Please provide a valid Property ID.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            try:
                property_obj = Property.objects.get(pk=pk)
            except Property.DoesNotExist:
                return Response({'error': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)
            property_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            Property.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
