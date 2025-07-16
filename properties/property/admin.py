from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Location, Amenity,PropertyImage, PropertyAmenity, Property, Land, Rental, CampusHostel, Apartment, Favorite, Review, Inquiry
# # Unregister the default User admin
# # admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user_type', 'bio', 'profile_picture')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'date_of_birth')
        }),
        ('Verification', {
            'fields': ('email_verified', 'phone_verified', 'identity_verified')
        }),
    )
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_user_type')
    list_select_related = ('profile',)

    def get_user_type(self, instance):
        return instance.profile.user_type
    get_user_type.short_description = 'User Type'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number', 'email_verified', 'phone_verified', 'identity_verified')
    list_filter = ('user_type', 'email_verified', 'phone_verified', 'identity_verified')
    search_fields = ('user__username', 'user__email', 'phone_number', 'company_name')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': ('user', 'user_type', 'bio', 'profile_picture')
            }),
            ('Contact Info', {
                'fields': ('phone_number', 'date_of_birth')
            }),
            ('Verification', {
                'fields': ('email_verified', 'phone_verified', 'identity_verified')
            }),
            
            ('Social Media', {
                'fields': ('facebook', 'twitter', 'instagram', 'linkedin'),
                'classes': ('collapse',)
            }),
            ('Location', {
                'fields': ('country', 'city', 'address'),
                'classes': ('collapse',)
            }),
        ]
        
        if obj:  # Only show metadata when editing existing profile
            fieldsets.append((
                'Metadata', {
                    'fields': ('created_at', 'updated_at', 'created_by', 'modified_by'),
                    'classes': ('collapse',)
                }
            ))
        return fieldsets
        # Custom display methods
    def phone_number_display(self, obj):
        return obj.phone_number if obj.phone_number else "Not set"
    phone_number_display.short_description = "Phone Number"

    def verification_status(self, obj):
        status = []
        if obj.email_verified:
            status.append("Email")
        if obj.phone_verified:
            status.append("Phone")
        if obj.identity_verified:
            status.append("ID")
        return ", ".join(status) if status else "Not verified"
    verification_status.short_description = "Verifications"

    # Handle the user field properly
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['created_at', 'updated_at']
        if obj:  # Editing an existing object
            return readonly_fields + ['user']
        return readonly_fields

    # Custom form handling
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Add form
            form.base_fields['user'].required = True
        return form

    # Custom save handling
    def save_model(self, request, obj, form, change):
        if not change and not obj.user_id:
            # Handle case where user isn't set (shouldn't happen with proper form)
            obj.user = request.user
        super().save_model(request, obj, form, change)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'country', 'region', 'city', 'district')
    list_filter = ('country', 'region', 'city')
    search_fields = ('country', 'region', 'city', 'district', 'street')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    readonly_fields = ('uploaded_at', 'updated_at')

class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 1
    readonly_fields = ('added_at', 'updated_at')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'property_type', 'owner', 'price', 'is_available', 'featured')
    list_filter = ('property_type', 'is_available', 'featured', 'price_period')
    search_fields = ('title', 'description', 'owner__user__username')
    readonly_fields = ('date_created', 'date_updated', 'views')
    inlines = [PropertyImageInline, PropertyAmenityInline]
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': ('owner', 'title', 'description', 'property_type')
            }),
            ('Pricing', {
                'fields': ('price', 'price_period')
            }),
            ('Status', {
                'fields': ('is_available', 'featured', 'views')
            }),
            ('Location', {
                'fields': ('location',)
            }),
            ('Management', {
                'fields': ('managed_by',),
                'classes': ('collapse',)
            }),
        ]
        
        if obj:
            fieldsets.append((
                'Metadata', {
                    'fields': ('date_created', 'date_updated', 'created_by', 'modified_by'),
                    'classes': ('collapse',)
                }
            ))
        return fieldsets

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'is_featured', 'uploaded_at')
    list_filter = ('is_featured',)
    readonly_fields = ('uploaded_at', 'updated_at')

@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):
    list_display = ('property', 'amenity', 'added_at')
    list_filter = ('amenity',)
    readonly_fields = ('added_at', 'updated_at')

# # Property Type Admins
@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ('property', 'land_type', 'area', 'has_utilities')
    list_filter = ('land_type', 'has_utilities')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ('property', 'rental_type', 'bedrooms', 'bathrooms', 'furnished')
    list_filter = ('rental_type', 'furnished')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('property', 'apartment_type', 'bedrooms', 'bathrooms', 'furnished')
    list_filter = ('apartment_type', 'furnished')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CampusHostel)
class CampusHostelAdmin(admin.ModelAdmin):
    list_display = ('property', 'hostel_type', 'room_type', 'capacity', 'meals_included')
    list_filter = ('hostel_type', 'room_type', 'meals_included')
    readonly_fields = ('created_at', 'updated_at')

# Interaction Admins
@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'date_added')
    list_filter = ('date_added',)
    readonly_fields = ('date_added', 'updated_at')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('property', 'user', 'status', 'date_sent', 'responded_at')
    list_filter = ('status', 'date_sent')
    readonly_fields = ('date_sent', 'updated_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('property', 'reviewer', 'rating', 'title', 'is_approved')
    list_filter = ('rating', 'is_approved')
    readonly_fields = ('created_at', 'updated_at')