from django.db import models
from django.utils.text import slugify
from django.core.mail import send_mail ,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import uuid
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.core.files.base import ContentFile
from .utils import generate_pdf
import os
from django.utils import timezone

class Hotel(models.Model):
    Hotel_Main_img = models.ImageField(upload_to='Hotel_img/', blank=True, null=True)
    Hotel_Name = models.CharField(max_length=255)
    Rating = models.DecimalField(max_digits=2, decimal_places=1)
    Stars = models.CharField(max_length=100)
    Hotel_Address = models.CharField(max_length=500)
    Fake_Price = models.IntegerField()
    Real_Price = models.IntegerField()
    Airport_pickup_price = models.IntegerField(default=0)   # new field
    Railway_pickup_price = models.IntegerField(default=0)   # new field
    Hotel_Overview = models.TextField()
    Hotel_L_Map_Embed_Code = models.TextField()
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.Hotel_Name)
            slug = base_slug
            counter = 1
            while Hotel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Hotel_Name
    


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="Hotel_imgs/")

    def __str__(self):
        return f"Image of {self.hotel.Hotel_Name}"


class HotelAmenity(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='amenities')
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - {self.hotel.Hotel_Name}"



# booking model 
class Booking(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    booking_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    room_quantity = models.PositiveIntegerField(default=1)
    railway_pickup = models.BooleanField(default=False)
    airport_pickup = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    location_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_contact_number = models.CharField(max_length=20, blank=True, null=True)
    admin_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"Booking #{self.booking_id} - {self.full_name}"

    def send_status_email(self):
        # Select subject and template based on booking status
        if self.status == self.CONFIRMED:
            subject = f"Your Booking Confirmation - {self.hotel.Hotel_Name}"
            template = 'emails/booking_confirmation'
        elif self.status == self.PENDING:
            subject = f"Your Booking is Pending - {self.hotel.Hotel_Name}"
            template = 'emails/booking_pending'
        elif self.status == self.CANCELLED:
            subject = f"Booking Cancellation - {self.hotel.Hotel_Name}"
            template = 'emails/booking_cancelled'
        else:
            return

        context = {
            'booking': self,
            'hotel': self.hotel,
        }

        # Render email content
        message = render_to_string(f'{template}.txt', context)
        html_message = render_to_string(f'{template}.html', context)

        # Create the email
        email = EmailMultiAlternatives(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email]
        )
        email.attach_alternative(html_message, "text/html")

        # If confirmed, generate PDF and attach
        if self.status == self.CONFIRMED:
            pdf_file = generate_pdf('emails/booking_confirmation_pdf.html', context)
            if pdf_file:
                email.attach(f'Booking_{self.booking_id}.pdf', pdf_file.getvalue(), 'application/pdf')

        email.send(fail_silently=False)

    def send_admin_notification(self):
        subject = f"New Booking Received - {self.hotel.Hotel_Name}"
        message = f"A new booking has been received:\n\nBooking ID: {self.booking_id}\nGuest: {self.full_name}\nHotel: {self.hotel.Hotel_Name}\nCheck-in: {self.check_in_date}\nCheck-out: {self.check_out_date}\nStatus: {self.get_status_display()}\n\nPlease log in to the admin panel to review."
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):
        # Check if status is being updated
        if self.pk:
            old_booking = Booking.objects.get(pk=self.pk)
            if old_booking.status != self.status:
                # Status changed, send appropriate email
                self.send_status_email()
        else:
            # New booking, send pending email
            super().save(*args, **kwargs)
            self.send_status_email()
            self.send_admin_notification()
            return
        
        super().save(*args, **kwargs)
