from django.contrib import admin
from .models import Location, Amenity, Property, PropertyAmenity, PropertyImage, Land, Rental, Apartment, CampusHostel, Favorite,  Inquiry, Profile, Review

# Register your models here.
admin.site.register(Location)
admin.site.register(Amenity)
admin.site.register(Property)
admin.site.register(PropertyAmenity)
admin.site.register(PropertyImage)
admin.site.register(Land)
admin.site.register(Rental)
admin.site.register(Apartment)
admin.site.register(CampusHostel)
admin.site.register(Favorite)
admin.site.register(Inquiry)
admin.site.register(Profile)
admin.site.register(Review)


