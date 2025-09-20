from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Hotel,HotelImage,HotelAmenity,Booking
from core.forms import ReviewForm
from core.models import Review
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from .forms import BookingForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages







def Hotels_View(request):
    hotel = Hotel.objects.all().order_by('-created_at')
    return render(request,'hotel.html',{'Hotel':hotel})





def hotel_detail_view(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    
    try:
        hotel_img = HotelImage.objects.filter(hotel=hotel)
    except HotelImage.DoesNotExist:
        hotel_img = None

    hotel_ami = HotelAmenity.objects.filter(hotel=hotel)

    # Handle review form
    if request.method == "POST" and 'review_form' in request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.content_type = ContentType.objects.get_for_model(Hotel)
            review.object_id = hotel.id
            review.save()
            messages.success(request, 'Your Review has been sent successfully!')
            return redirect('hotel_detail', slug=hotel.slug)
    else:
        form = ReviewForm()

    # Handle booking form
    if request.method == "POST" and 'booking_form' in request.POST:
        booking_form = BookingForm(request.POST, hotel=hotel)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.hotel = hotel
            
            # Calculate number of nights
            check_in = booking.check_in_date
            check_out = booking.check_out_date
            nights = (check_out - check_in).days
            if nights <= 0:
                messages.error(request, 'Check-out date must be after check-in date')
                return redirect('hotel_detail', slug=hotel.slug)
            
            # Get room quantity
            quantity = int(request.POST.get('quantity', 1))
            
            # Calculate base price
            base_price = hotel.Real_Price * nights * quantity
            
            # Calculate services
            railway_pickup = 'railway' in request.POST.getlist('services_list[]')
            airport_pickup = 'airport' in request.POST.getlist('services_list[]')
            
            extra_services = 0
            if railway_pickup:
                extra_services += hotel.Railway_pickup_price
                booking.railway_pickup = True
            if airport_pickup:
                extra_services += hotel.Airport_pickup_price
                booking.airport_pickup = True
            
            # Set calculated total price
            booking.total_price = base_price + extra_services
            booking.save()
            
            messages.success(request, 'Booking submitted successfully! You will receive a confirmation email shortly.')
            return redirect('booking_pending', booking_id=booking.booking_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        booking_form = BookingForm(hotel=hotel)

    context = {
        'hotel': hotel,
        'hotel_img': hotel_img,
        'hotel_amenity': hotel_ami,
        'form': form,
        'booking_form': booking_form,
    }
    return render(request, 'hotel-details.html', context)


def booking_pending(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    context = {
        'booking': booking
    }
    return render(request, 'booking_pending.html', context)
