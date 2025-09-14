from django.contrib import admin
from django.conf import settings
from django.core.mail import send_mail
from .models import HomeSection,TopPalace,Review,WhyChooseSection,Destination,AboutSection,ContactSubmission
from Hotel.models import Hotel, HotelImage, HotelAmenity,Booking
from Camping.models import Camping_Tent, CampingImage, CampingHighlight, CampingInclusion, CampingExclusion,CampBooking
from Adventure.models import Activity, ActivityImage, ActivityHighlight, ActivityInclusion, ActivityExclusion,ActivityBooking




@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ('short_heading', 'highlight_text')


@admin.register(TopPalace)
class TopPalaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')




@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ( "branches_count", "destinations_count", "customers_count", "updated_at")


@admin.register(WhyChooseSection)
class WhyChooseSectionAdmin(admin.ModelAdmin):
    list_display = ('heading',)
    

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance_from_jaisalmer')
    search_fields = ('name',)



# Inline form for multiple images
class HotelImageInline(admin.StackedInline):
    model = HotelImage
    extra = 1   # 1 empty form by default

# Inline form for amenities
class HotelAmenityInline(admin.StackedInline):
    model = HotelAmenity
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('Hotel_Name', 'Stars', 'Real_Price', 'slug')
    list_filter = ('Stars',)
    search_fields = ('Hotel_Name', 'Hotel_Address')
    prepopulated_fields = {'slug': ('Hotel_Name',)}

    # Show inlines inside hotel form
    inlines = [HotelImageInline, HotelAmenityInline]






# Inline classes - ye related models ko main form ke andar hi dikhayenge
class CampingImageInline(admin.TabularInline):   # ya StackedInline bhi use kar sakte ho
    model = CampingImage
    extra = 1


class CampingHighlightInline(admin.TabularInline):
    model = CampingHighlight
    extra = 1


class CampingInclusionInline(admin.TabularInline):
    model = CampingInclusion
    extra = 1


class CampingExclusionInline(admin.TabularInline):
    model = CampingExclusion
    extra = 1


# Main admin class
@admin.register(Camping_Tent)
class CampingTentAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Rating', 'Real_Price', 'slug')
    search_fields = ('Name', 'Address')
    list_filter = ('Rating',)
    prepopulated_fields = {'slug': ('Name',)}  # Slug automatically Name se generate hoga
    inlines = [
        CampingImageInline,
        CampingHighlightInline,
        CampingInclusionInline,
        CampingExclusionInline
    ]









class ActivityImageInline(admin.TabularInline):
    model = ActivityImage
    extra = 1

class ActivityHighlightInline(admin.TabularInline):
    model = ActivityHighlight
    extra = 1

class ActivityInclusionInline(admin.TabularInline):
    model = ActivityInclusion
    extra = 1

class ActivityExclusionInline(admin.TabularInline):
    model = ActivityExclusion
    extra = 1

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Rating', 'location', 'Real_price', 'slug')
    search_fields = ('Name', 'location', 'Address')
    list_filter = ('location', 'Rating')
    prepopulated_fields = {'slug': ('Name',)}
    inlines = [ActivityImageInline, ActivityHighlightInline, ActivityInclusionInline, ActivityExclusionInline]



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'content_type', 'object_id', 'approved', 'created_at')
    list_filter = ('approved', 'content_type', 'created_at')
    search_fields = ('name', 'email', 'description')
    list_editable = ('approved',)



# contact 

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submission_date', 'agreed_to_terms')
    list_filter = ('submission_date', 'agreed_to_terms')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('submission_date',)


# booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'hotel', 'full_name', 'email', 'check_in_date', 'check_out_date', 'status', 'admin_contact_number')
    list_filter = ('status', 'hotel')
    search_fields = ('booking_id', 'full_name', 'email', 'admin_contact_number')
    readonly_fields = ('booking_id', 'created_at', 'updated_at')
    
    # Add these fields to control what admins see in add/change forms
    fieldsets = (
        (None, {
            'fields': ('booking_id', 'hotel', 'status')
        }),
        ('Guest Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('check_in_date', 'check_out_date', 'room_quantity', 
                      'railway_pickup', 'airport_pickup', 'total_price')
        }),
        ('Admin Details', {
            'fields': ('room_number', 'location_url', 'admin_contact_number', 'admin_email'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # First save the model to ensure we have a PK
        super().save_model(request, obj, form, change)
        
        # Set admin contact details if they're not set
        if not hasattr(obj, 'admin_contact_number') or not obj.admin_contact_number:
            obj.admin_contact_number = settings.ADMIN_CONTACT_NUMBER  # Add to settings.py
        if not hasattr(obj, 'admin_email') or not obj.admin_email:
            obj.admin_email = settings.ADMIN_EMAIL
        
        # Save again to store admin details
        obj.save()
        
        # Check for status changes and send appropriate emails
        if change:
            original_obj = Booking.objects.get(pk=obj.pk)
            if original_obj.status != obj.status:
                obj.send_status_email()
                
                # Additional notification for admin when status changes to confirmed
                if obj.status == 'confirmed':
                    self.send_admin_confirmation_notification(obj)

    def send_admin_confirmation_notification(self, booking):
        subject = f"Booking Confirmed - {booking.hotel.Hotel_Name} (ID: {booking.booking_id})"
        message = (
            f"Booking has been confirmed:\n\n"
            f"Guest: {booking.full_name}\n"
            f"Hotel: {booking.hotel.Hotel_Name}\n"
            f"Dates: {booking.check_in_date} to {booking.check_out_date}\n"
            f"Contact: {booking.phone}\n"
            f"Admin Contact: {booking.admin_contact_number}\n\n"
            f"Please ensure room preparation."
        )
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [booking.admin_email, settings.ADMIN_EMAIL],
            fail_silently=False,
        )









# camp booking 


@admin.register(CampBooking)
class CampBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'camp', 'full_name', 'email', 'check_in_date', 'check_out_date', 'status', 'admin_contact_number')
    list_filter = ('status', 'camp')
    search_fields = ('booking_id', 'full_name', 'email', 'phone', 'admin_contact_number')
    readonly_fields = ('booking_id', 'created_at', 'updated_at', 'total_price')
    list_editable = ('status', 'admin_contact_number')
    
    fieldsets = (
        (None, {
            'fields': ('booking_id', 'camp', 'status', 'total_price')
        }),
        ('Guest Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('check_in_date', 'check_out_date', 'quantity')
        }),
        ('Pickup Services', {
            'fields': ('pickup_home', 'pickup_hotel', 'pickup_railway', 'pickup_airport'),
            'classes': ('collapse',)
        }),
        ('Admin Details', {
            'fields': ('camp_number', 'location_url', 'admin_contact_number', 'admin_email'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        # Calculate total price if not set
        if not obj.total_price:
            obj.total_price = obj.camp.Real_Price * obj.quantity
            if obj.pickup_home:
                obj.total_price += obj.camp.Pickup_Home_Price
            if obj.pickup_hotel:
                obj.total_price += obj.camp.Pickup_Hotel_Price
            if obj.pickup_railway:
                obj.total_price += obj.camp.Pickup_Railway_Station_Price
            if obj.pickup_airport:
                obj.total_price += obj.camp.Pickup_Airport_Price
        
        super().save_model(request, obj, form, change)










@admin.register(ActivityBooking)
class ActivityBookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'activity', 'full_name', 'email', 'booking_date', 'status', 'admin_contact_number')
    list_filter = ('status', 'activity')
    search_fields = ('booking_id', 'full_name', 'email', 'phone', 'admin_contact_number')
    readonly_fields = ('booking_id', 'created_at', 'updated_at', 'total_price')
    list_editable = ('status', 'admin_contact_number')
    
    fieldsets = (
        (None, {
            'fields': ('booking_id', 'activity', 'status', 'total_price')
        }),
        ('Guest Information', {
            'fields': ('full_name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('booking_date', 'quantity')
        }),
        ('Pickup Services', {
            'fields': ('pickup_home', 'pickup_hotel', 'pickup_railway', 'pickup_airport'),
            'classes': ('collapse',)
        }),
        ('Admin Details', {
            'fields': ('location_url', 'admin_contact_number', 'admin_email'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.total_price:
            obj.total_price = obj.activity.Real_price * obj.quantity
            if obj.pickup_home:
                obj.total_price += obj.activity.Pickup_Home_Price
            if obj.pickup_hotel:
                obj.total_price += obj.activity.Pickup_Hotel_Price
            if obj.pickup_railway:
                obj.total_price += obj.activity.Pickup_Railway_Station_Price
            if obj.pickup_airport:
                obj.total_price += obj.activity.Pickup_Airport_Price
        
        super().save_model(request, obj, form, change)