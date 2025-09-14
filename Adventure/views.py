from django.shortcuts import render
from Adventure.models import Activity,ActivityBooking
from django.shortcuts import render, get_object_or_404
from core.forms import ReviewForm
from core.models import Review
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect




def Activities(request):
    adventure = Activity.objects.all().order_by('-created_at')
    return render(request ,'activity-list.html',{'Adventrue':adventure})



# Activities Details 
def Activity_Details_View(request, slug):
    activity = get_object_or_404(Activity, slug=slug)
    images = activity.images.first()  
    highlights = activity.highlights.all()
    inclusions = activity.inclusions.all()
    exclusions = activity.exclusions.all()

    # Filter reviews for this activity
    content_type = ContentType.objects.get_for_model(Activity)
    reviews = Review.objects.filter(content_type=content_type, object_id=activity.id, approved=True)

    # Handle review form
    if request.method == "POST":
        if 'review_form' in request.POST:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.content_type = content_type
                review.object_id = activity.id
                review.save()
                return redirect('activity_detail', slug=activity.slug)
        else:
            form = ReviewForm()

        # Handle booking form submission
        if 'booking_form' in request.POST:
            # Create booking from form data
            booking = ActivityBooking(
                activity=activity,
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                booking_date=request.POST.get('check_in_date'),
                quantity=int(request.POST.get('quantity', 1)),
                pickup_home='0' in request.POST.getlist('services_list[]'),
                pickup_hotel='1' in request.POST.getlist('services_list[]'),
                pickup_railway='2' in request.POST.getlist('services_list[]'),
                pickup_airport='3' in request.POST.getlist('services_list[]'),
            )
            
            # Calculate total price
            total_price = activity.Real_price * booking.quantity
            if booking.pickup_home:
                total_price += activity.Pickup_Home_Price
            if booking.pickup_hotel:
                total_price += activity.Pickup_Hotel_Price
            if booking.pickup_railway:
                total_price += activity.Pickup_Railway_Station_Price
            if booking.pickup_airport:
                total_price += activity.Pickup_Airport_Price
            
            booking.total_price = total_price
            booking.save()
            
            # Redirect to success page or same page with success message
            return redirect('activity_booking_pending', booking_id=booking.booking_id)
    else:
        form = ReviewForm()

    context = {
        'activity': activity,
        'images': images,
        'highlights': highlights,
        'inclusions': inclusions,
        'exclusions': exclusions,
        'form': form,
        'reviews': reviews,
    }
    return render(request, 'activities-details.html', context)





def activity_booking_pending(request, booking_id):
    booking = get_object_or_404(ActivityBooking, booking_id=booking_id)
    return render(request, 'activity_pending.html', {'booking': booking})