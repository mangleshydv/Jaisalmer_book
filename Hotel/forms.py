from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    services_list = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Booking
        fields = ['full_name', 'email', 'phone', 'check_in_date', 'check_out_date', 
                 'room_quantity', 'total_price']
    
    def __init__(self, *args, **kwargs):
        hotel = kwargs.pop('hotel', None)
        super().__init__(*args, **kwargs)
        if hotel:
            self.fields['services_list'].choices = [
                ('railway', f"Railway Station Pickup (₹{hotel.Railway_pickup_price})"),
                ('airport', f"Airport Pickup (₹{hotel.Airport_pickup_price})")
            ]