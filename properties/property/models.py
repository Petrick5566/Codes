from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator


class Location(models.Model):
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        unique_together = ('country', 'region', 'city', 'district', 'street')

    def __str__(self):
        parts = [self.street, self.district, self.city, self.region, self.country]
        return ', '.join(filter(None, parts))

class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name
# Create your models here.


class Property(models.Model):
    PROPERTY_TYPES = [
        ('LAND', 'Land'),
        ('RENTAL', 'Rental'),
        ('APARTMENT', 'Apartment'),
        ('HOSTEL', 'Campus Hostel'),
    ]
    PRICE_PERIODS = [
        ('ONETIME', 'One-time'),
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    price_period = models.CharField(max_length=20, choices=PRICE_PERIODS, default='ONETIME')
    is_available = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    amenities = models.ManyToManyField(Amenity, through='PropertyAmenity', related_name='properties')

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} - {self.property_type}"


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    notes = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        unique_together = ('property', 'amenity')
        verbose_name_plural = 'Property amenities'

    def __str__(self):
        return f"{self.property.title} - {self.amenity.name}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    is_featured = models.BooleanField(default=False)
    caption = models.CharField(max_length=100, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"

class Land(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True)
    land_type = models.CharField(max_length=20, choices=[
        ('RESIDENTIAL', 'Residential'),
        ('COMMERCIAL', 'Commercial'),
        ('AGRICULTURAL', 'Agricultural'),
        ('INDUSTRIAL', 'Industrial'),
        ('OTHER', 'Other'),
    ])
    area = models.DecimalField(max_digits=10, decimal_places=2)
    zoning = models.CharField(max_length=100, blank=True, null=True)
    has_utilities = models.BooleanField(default=False)
    topographical_features = models.TextField(blank=True, null=True)

class Rental(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True)
    rental_type = models.CharField(max_length=20, choices=[
        ('HOUSE', 'House'),
        ('TOWNHOUSE', 'Townhouse'),
        ('VILLA', 'Villa'),
        ('COTTAGE', 'Cottage'),
        ('OTHER', 'Other'),
    ])
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    floors = models.PositiveIntegerField(default=1)
    furnished = models.BooleanField(default=False)
    parking_spaces = models.PositiveIntegerField(default=0)
    year_built = models.PositiveIntegerField(blank=True, null=True)


class Apartment(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True)
    apartment_type = models.CharField(max_length=20, choices=[
        ('STUDIO', 'Studio'),
        ('1BED', '1 Bedroom'),
        ('2BED', '2 Bedrooms'),
        ('3BED', '3 Bedrooms'),
        ('PENTHOUSE', 'Penthouse'),
        ('DUPLEX', 'Duplex'),
    ])
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    floor_number = models.PositiveIntegerField()
    total_floors = models.PositiveIntegerField()
    furnished = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)
    year_built = models.PositiveIntegerField(blank=True, null=True)
    building_name = models.CharField(max_length=100, blank=True, null=True)


class CampusHostel(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True)
    hostel_type = models.CharField(max_length=20, choices=[
        ('MALE', 'Male Hostel'),
        ('FEMALE', 'Female Hostel'),
        ('MIXED', 'Mixed Hostel'),
    ])
    room_type = models.CharField(max_length=20, choices=[
        ('SINGLE', 'Single Room'),
        ('SHARED', 'Shared Room'),
        ('DORM', 'Dormitory'),
    ])
    capacity = models.PositiveIntegerField()
    meals_included = models.BooleanField(default=False)
    distance_to_campus = models.DecimalField(max_digits=5, decimal_places=2)
    curfew_time = models.TimeField(blank=True, null=True)
    has_laundry = models.BooleanField(default=False)
    has_study_room = models.BooleanField(default=False)


# --- Interaction Models ---

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'property')
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.user.username}'s favorite: {self.property.title}"


class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    responded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_sent']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry about {self.property.title} from {self.user.username}"