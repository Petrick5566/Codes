from rest_framework import serializers
from .models import Property, Location, Amenity, PropertyAmenity, PropertyImage, Land, Rental, Apartment, CampusHostel, Favorite, Inquiry

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class CampusHostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class Inquiryerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

