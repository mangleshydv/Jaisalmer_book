# forms.py
from django import forms
from .models import ActivityBooking

class ActivityBookingForm(forms.ModelForm):
    SERVICES_CHOICES = [
        ('home', 'Pickup From Home'),
        ('hotel', 'Pickup From Hotel'),
        ('railway', 'Pickup From Railway Station'),
        ('airport', 'Pickup From Airport'),
    ]
    
    services = forms.MultipleChoiceField(
        choices=SERVICES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = ActivityBooking
        fields = ['full_name', 'email', 'phone', 'booking_date', 'quantity']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.activity = kwargs.pop('activity', None)
        super().__init__(*args, **kwargs)
        
        if self.activity:
            # Set initial quantity to 1
            self.fields['quantity'].initial = 1
            # Set min/max for quantity based on group size
            self.fields['quantity'].widget.attrs.update({
                'min': 1,
                'max': self.activity.Group_size,
            })
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1")
        if self.activity and quantity > self.activity.Group_size:
            raise forms.ValidationError(f"Maximum group size is {self.activity.Group_size}")
        return quantity
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.activity = self.activity
        
        # Calculate total price
        quantity = self.cleaned_data.get('quantity', 1)
        base_price = self.activity.Real_price * quantity
        total_price = base_price
        
        # Process services
        services = self.cleaned_data.get('services', [])
        instance.pickup_home = 'home' in services
        instance.pickup_hotel = 'hotel' in services
        instance.pickup_railway = 'railway' in services
        instance.pickup_airport = 'airport' in services
        
        # Add service prices to total
        if instance.pickup_home:
            total_price += self.activity.Pickup_Home_Price
        if instance.pickup_hotel:
            total_price += self.activity.Pickup_Hotel_Price
        if instance.pickup_railway:
            total_price += self.activity.Pickup_Railway_Station_Price
        if instance.pickup_airport:
            total_price += self.activity.Pickup_Airport_Price
        
        instance.total_price = total_price
        instance.location_url = self.activity.location
        
        if commit:
            instance.save()
        return instance