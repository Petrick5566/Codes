from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PropertImage
from .serializers import PropertyImageSerializer

class PropertyImageView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                image = PropertyImage.objects.get(pk=pk)
            except PropertyImage.DoesNotExist:
                return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = PropertyImageSerializer(image)
            return Response(serializer.data)
        images = PropertyImage.objects.all()
        serializer = PropertyImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertyImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            image = PropertyImage.objects.get(pk=pk)
        except PropertyImage.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)