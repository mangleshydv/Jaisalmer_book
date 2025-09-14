from django.shortcuts import render, get_object_or_404
from Camping.models import Camping_Tent,CampingExclusion,CampingImage,CampingHighlight,CampingInclusion,CampBooking
from core.forms import ReviewForm
from core.models import Review
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
# Create your views here.
# Camping list
def Camping(request):
    camping_data = Camping_Tent.objects.all().order_by('-created_at')
    return render(request,'package-grid.html',{'Camping':camping_data})



def Camping_Details(request, slug):
    camp = get_object_or_404(Camping_Tent, slug=slug)
    images = CampingImage.objects.filter(camp=camp).first()
    highlights = CampingHighlight.objects.filter(camp=camp)
    inclusions = CampingInclusion.objects.filter(camp=camp)
    exclusions = CampingExclusion.objects.filter(camp=camp)

    # Filter reviews for this hotel
    content_type = ContentType.objects.get_for_model(Camping_Tent)
    reviews = Review.objects.filter(content_type=content_type, object_id=camp.id, approved=True)

    # Handle review form
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.content_type = content_type
            review.object_id = camp.id
            review.save()
            return redirect('camp_detail', slug=camp.slug)
    else:
        form = ReviewForm()

    if request.method == 'POST' and 'CampBookingForm' in request.POST:
        # Get form data
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        quantity = int(request.POST.get('quantity', 1))
        
        # Calculate number of nights
        from datetime import datetime
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        nights = (check_out - check_in).days
        
        if nights <= 0:
            # Handle invalid date range
            messages.error(request, "Check-out date must be after check-in date")
            return redirect('camp_detail', slug=camp.slug)
        
        # Create booking from form data
        booking = CampBooking(
            camp=camp,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            quantity=quantity,
            pickup_home='0' in request.POST.getlist('services_list[]'),
            pickup_hotel='1' in request.POST.getlist('services_list[]'),
            pickup_railway='2' in request.POST.getlist('services_list[]'),
            pickup_airport='3' in request.POST.getlist('services_list[]'),
        )
        
        # Calculate total price - IMPORTANT: Multiply by number of nights
        total_price = camp.Real_Price * quantity * nights
        
        if booking.pickup_home:
            total_price += camp.Pickup_Home_Price
        if booking.pickup_hotel:
            total_price += camp.Pickup_Hotel_Price
        if booking.pickup_railway:
            total_price += camp.Pickup_Railway_Station_Price
        if booking.pickup_airport:
            total_price += camp.Pickup_Airport_Price
        
        booking.total_price = total_price
        booking.save()
        
        return redirect('camp_booking_pending', booking_id=booking.booking_id)

    context = {
        'camp': camp,
        'images': images,
        'highlights': highlights,
        'inclusions': inclusions,
        'exclusions': exclusions,
        'form': form,
        'reviews': reviews,
    }
    return render(request, 'package-details.html', context)








def camp_booking_pending(request, booking_id):
    booking = get_object_or_404(CampBooking, booking_id=booking_id)
    return render(request, "camp_booking_pending.html", {"booking": booking})