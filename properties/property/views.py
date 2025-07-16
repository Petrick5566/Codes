from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Property, Favorite, Inquiry, Review, User
from .serializers import PropertySerializer, FavoriteSerializer, InquirySerializer, ReviewSerializer
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, ProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

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

class FavoriteView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                favorite = Favorite.objects.get(pk=pk)
            except Favorite.DoesNotExist:
                return Response({'error': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = FavoriteSerializer(favorite)
            return Response(serializer.data)
        favorites = Favorite.objects.filter(user=request.user.profile)
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.profile.id
        serializer = FavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            favorite = Favorite.objects.get(pk=pk, user=request.user.profile)
        except Favorite.DoesNotExist:
            return Response({'error': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InquiryView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                inquiry = Inquiry.objects.get(pk=pk)
            except Inquiry.DoesNotExist:
                return Response({'error': 'Inquiry not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = InquirySerializer(inquiry)
            return Response(serializer.data)
        inquiries = Inquiry.objects.filter(user=request.user.profile)
        serializer = InquirySerializer(inquiries, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.profile.id
        serializer = InquirySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                review = Review.objects.get(pk=pk)
            except Review.DoesNotExist:
                return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        reviews = Review.objects.filter(reviewer=request.user.profile)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['reviewer'] = request.user.profile.id
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            profile = ProfileSerializer(user.profile)
            
            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                },
                'profile': profile.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            user = User.objects.get(username=request.data['username'])
            profile = ProfileSerializer(user.profile)
            
            response.data['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            response.data['profile'] = profile.data
            
        return response
# Create your views here.
