from django import forms
from .models import Review,ContactSubmission

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'email', 'description']





class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'phone', 'email', 'message', 'agreed_to_terms']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Name',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+91-0737 621 432',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'hello@example.com',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Leave your message...',
                'rows': 4,
                'class': 'form-control'
            }),
            'agreed_to_terms': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'agreed_to_terms': 'Agree to our <span>Terms of service</span> and <span>Privacy Policy</span>'
        }

