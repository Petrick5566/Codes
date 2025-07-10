from rest_framework import serializers
from .models import Property, Location, Amenity, PropertyAmenity, PropertyImage, Land, Rental, Apartment, CampusHostel, Favorite, Inquiry

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

# from .models import Amenity

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyAmenity
        fields = '__all__'


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = '__all__'

class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        fields = '__all__'

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model =Rental
        fields = '__all__'

class CampusHostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusHostel
        fields = '__all__'

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'

