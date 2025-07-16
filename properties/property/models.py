from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings


# from property.models import Profile, property

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
class Profile(models.Model):
    USER_TYPES = [
        ('INDIVIDUAL', 'Individual'),
        ('AGENT', 'Agent'),
        ('AGENCY', 'Agency'),
        ('DEVELOPER', 'Developer'),
        ('LANDLORD', 'Landlord'),
        ('STUDENT', 'Student'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='INDIVIDUAL')
    bio = models.TextField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    identity_verified = models.BooleanField(default=False)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_profiles')
    modified_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_profiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    # Social media links
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    
    # Location information
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # For the first user (superuser), created_by will be None
        Profile.objects.create(user=instance)


class Location(models.Model):
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_locations')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_locations')

    class Meta:
        unique_together = ('country', 'region', 'city', 'district', 'street')

    def __str__(self):
        parts = [self.street, self.district, self.city, self.region, self.country]
        return ', '.join(filter(None, parts))


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_amenities')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_amenities')

    def __str__(self):
        return self.name


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

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='properties')
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
    managed_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, 
                                 related_name='managed_properties')
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_properties')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_properties')

    class Meta:
        ordering = ['-date_created']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return f"{self.title} - {self.property_type}"


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)
    notes = models.CharField(max_length=100, blank=True, null=True)
    added_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    added_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='added_property_amenities')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_property_amenities')

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
    uploaded_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    uploaded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='uploaded_property_images')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_property_images')

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
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_land_properties')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_land_properties')


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
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_rental_properties')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_rental_properties')


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
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_apartment_properties')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_apartment_properties')


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
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_hostel_properties')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_hostel_properties')


class Favorite(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_favorites')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_favorites')

    class Meta:
        unique_together = ('user', 'property')
        ordering = ['-date_added']

    def __str__(self):
        return f"{self.user.user.username}'s favorite: {self.property.title}"


class Inquiry(models.Model):
    INQUIRY_STATUS = [
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='inquiries' )
    message = models.TextField()
    contact_phone = PhoneNumberField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    status = models.CharField(max_length=20, choices=INQUIRY_STATUS, default='NEW')
    responded_at = models.DateTimeField(blank=True, null=True)
    responded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='responded_inquiries')
    response_notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_inquiries')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_inquiries')

    class Meta:
        ordering = ['-date_sent']
        verbose_name_plural = 'Inquiries'

    def __str__(self):
        return f"Inquiry about {self.property.title} from {self.user.user.username}"


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    response = models.TextField(blank=True, null=True)
    responded_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='review_responses')
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='created_reviews')
    modified_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_reviews')

    class Meta:
        ordering = ['-created_at']
        unique_together = ('property', 'reviewer')

    def __str__(self):
        return f"Review by {self.reviewer.user.username} for {self.property.title}"