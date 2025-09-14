from django.db import models
from django.utils.text import slugify
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.contenttypes.models import ContentType
import uuid
from django.template.loader import render_to_string
from django.conf import settings
from io import BytesIO
from django.template.loader import get_template
from weasyprint import HTML
from django.core.files.base import ContentFile
import os
from Hotel.utils import generate_pdf
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.files import File




# Camping Tents
class Camping_Tent(models.Model):
    Name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=250, unique=True, blank=True) 
    Features = models.CharField(max_length=100)
    Rating = models.DecimalField(max_digits=2, decimal_places=1)
    Address = models.CharField(max_length=500)
    Days = models.IntegerField()
    Night = models.IntegerField()
    Fake_Price = models.IntegerField()
    Real_Price = models.IntegerField()
    Overviwe = models.TextField()
    Embed_code = models.TextField(blank=True, null=True) 
    Main_Image = models.ImageField(upload_to='camping/', blank=True, null=True)

    Pickup_Home_Price = models.IntegerField(blank=True, null=True)
    Pickup_Hotel_Price = models.IntegerField(blank=True, null=True)
    Pickup_Railway_Station_Price = models.IntegerField(blank=True, null=True)
    Pickup_Airport_Price = models.IntegerField(blank=True, null=True)

    Single_Camp_People = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.Name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Name)[:250]
        super().save(*args, **kwargs)


class CampingImage(models.Model):
    camp = models.ForeignKey(Camping_Tent, on_delete=models.CASCADE, related_name='images')
    image1 = models.ImageField(upload_to='camping/images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='camping/images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='camping/images/', blank=True, null=True)
    image4 = models.ImageField(upload_to='camping/images/', blank=True, null=True)
    image5 = models.ImageField(upload_to='camping/images/', blank=True, null=True)

    def __str__(self):
        return f"Image for {self.camp.Name}"


class CampingHighlight(models.Model):
    camp = models.ForeignKey(Camping_Tent, on_delete=models.CASCADE, related_name='highlights')
    point = models.CharField(max_length=500)

    def __str__(self):
        return self.point


class CampingInclusion(models.Model):
    camp = models.ForeignKey(Camping_Tent, on_delete=models.CASCADE, related_name='inclusions')
    point = models.CharField(max_length=500)

    def __str__(self):
        return self.point


class CampingExclusion(models.Model):
    camp = models.ForeignKey(Camping_Tent, on_delete=models.CASCADE, related_name='exclusions')
    point = models.CharField(max_length=500)

    def __str__(self):
        return self.point









class CampBooking(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    booking_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    camp = models.ForeignKey('Camping_Tent', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    pickup_home = models.BooleanField(default=False)
    pickup_hotel = models.BooleanField(default=False)
    pickup_railway = models.BooleanField(default=False)
    pickup_airport = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    camp_number = models.CharField(max_length=20, blank=True, null=True)
    location_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_contact_number = models.CharField(max_length=20, blank=True, null=True)
    admin_email = models.EmailField(blank=True, null=True)
    confirmation_pdf = models.FileField(upload_to='booking_pdfs/', blank=True, null=True)

    def __str__(self):
        return f"Booking #{self.booking_id} - {self.full_name}"

    def get_services(self):
        services = []
        if self.pickup_home:
            services.append(f"Home Pickup (₹{self.camp.Pickup_Home_Price})")
        if self.pickup_hotel:
            services.append(f"Hotel Pickup (₹{self.camp.Pickup_Hotel_Price})")
        if self.pickup_railway:
            services.append(f"Railway Pickup (₹{self.camp.Pickup_Railway_Station_Price})")
        if self.pickup_airport:
            services.append(f"Airport Pickup (₹{self.camp.Pickup_Airport_Price})")
        return services

    def generate_confirmation_pdf(self):
        """Generate PDF confirmation for the booking using WeasyPrint"""
        template_path = 'emails/camp_booking_pdf.html'
        context = {
            'booking': self,
            'camp': self.camp,
            'services': self.get_services(),
        }
        
        html_string = render_to_string(template_path, context)

        # Save directory
        pdf_dir = os.path.join(settings.MEDIA_ROOT, 'booking_pdfs')
        os.makedirs(pdf_dir, exist_ok=True)

        filename = f'booking_confirmation_{self.booking_id}.pdf'
        filepath = os.path.join(pdf_dir, filename)

        # ✅ Generate PDF with WeasyPrint
        HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf(filepath)

        # Save file without calling save() again
        self.confirmation_pdf.save(filename, File(open(filepath, 'rb')), save=False)
        return True

    def send_status_email(self):
        """Send status-based email to customer"""
        # Determine email subject & template
        if self.status == self.CONFIRMED:
            subject = f"Your Camp Booking Confirmation - {self.camp.Name}"
            template = 'emails/camp_booking_confirmation'
            # Generate PDF if not exists
            if not self.confirmation_pdf:
                self.generate_confirmation_pdf()
                self.save(update_fields=['confirmation_pdf'])
        elif self.status == self.PENDING:
            subject = f"Your Camp Booking is Pending - {self.camp.Name}"
            template = 'emails/camp_booking_pending'
        elif self.status == self.CANCELLED:
            subject = f"Camp Booking Cancellation - {self.camp.Name}"
            template = 'emails/camp_booking_cancelled'
        else:
            return

        context = {
            'booking': self,
            'camp': self.camp,
            'services': self.get_services(),
        }

        message = render_to_string(f'{template}.txt', context)
        html_message = render_to_string(f'{template}.html', context)

        # Add dynamic header color in HTML
        if self.status == self.CONFIRMED:
            html_message = html_message.replace('<!--STATUS_HEADER-->',
                'background: linear-gradient(135deg, #4caf50, #81c784);')  # Green
        elif self.status == self.PENDING:
            html_message = html_message.replace('<!--STATUS_HEADER-->',
                'background: linear-gradient(135deg, #ff9800, #ffb74d);')  # Orange
        elif self.status == self.CANCELLED:
            html_message = html_message.replace('<!--STATUS_HEADER-->',
                'background: linear-gradient(135deg, #e53935, #ef5350);')  # Red

        email = EmailMultiAlternatives(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email]
        )
        email.attach_alternative(html_message, "text/html")

        if self.status == self.CONFIRMED and self.confirmation_pdf:
            email.attach_file(self.confirmation_pdf.path)

        email.send(fail_silently=False)

    def send_admin_notification(self):
        """Send only on new booking"""
        subject = f"New Camp Booking Received - {self.camp.Name}"
        message = (
            f"A new camp booking has been received:\n\n"
            f"Booking ID: {self.booking_id}\n"
            f"Guest: {self.full_name}\n"
            f"Camp: {self.camp.Name}\n"
            f"Check-in: {self.check_in_date}\n"
            f"Check-out: {self.check_out_date}\n"
            f"Status: {self.get_status_display()}\n\n"
            f"Please log in to the admin panel to review."
        )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        old_status = None

        if not is_new:
            old_status = CampBooking.objects.filter(pk=self.pk).values_list('status', flat=True).first()

        super().save(*args, **kwargs)

        # Ensure admin contact details are set
        update_fields = []
        if not self.admin_contact_number:
            self.admin_contact_number = settings.ADMIN_CONTACT_NUMBER
            update_fields.append('admin_contact_number')
        if not self.admin_email:
            self.admin_email = settings.ADMIN_EMAIL
            update_fields.append('admin_email')
        if update_fields:
            super().save(update_fields=update_fields)

        # Email triggers
        if is_new:
            # New booking → Admin notification
            self.send_admin_notification()
            # New booking → User gets Pending email immediately
            self.send_status_email()
        elif old_status != self.status:
            # Status change → Only user gets email
            self.send_status_email()
