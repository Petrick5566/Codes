# Codes
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'phone_number_display', 'verification_status')
    list_filter = ('user_type', 'email_verified', 'phone_verified', 'identity_verified')
    search_fields = ('user__username', 'user__email', 'phone_number', 'company_name')
    
    # Fields configuration
    fieldsets = (
        (None, {
            'fields': ('user', 'user_type')
        }),
        ('Personal Info', {
            'fields': ('bio', 'profile_picture', 'date_of_birth')
        }),
        ('Contact Info', {
            'fields': ('phone_number',)
        }),
        ('Professional Info', {
            'fields': ('license_number', 'company_name', 'website'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin'),
            'classes': ('collapse',)
        }),
        ('Location', {
            'fields': ('country', 'city', 'address'),
            'classes': ('collapse',)
        }),
        ('Verification', {
            'fields': ('email_verified', 'phone_verified', 'identity_verified'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

