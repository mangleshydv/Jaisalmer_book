from django.shortcuts import render,redirect
from .models import HomeSection,TopPalace,Review,WhyChooseSection,Destination,AboutSection,ContactSubmission
from Hotel.models import Hotel
from Camping.models import Camping_Tent
from Adventure.models import Activity
from .forms import ContactForm
from django.contrib import messages



# Create your views here.

def Home_View(request):
    home_sections = HomeSection.objects.first()
    palaces = TopPalace.objects.all()
    whychoose = WhyChooseSection.objects.first()
    destinations = Destination.objects.all()
    hotels = Hotel.objects.all()[:9]
    camps = Camping_Tent.objects.all().order_by('-created_at')[:9]
    activities = Activity.objects.all().order_by('-created_at')[:9]
    reviews = Review.objects.filter(approved=True).order_by('-created_at')[:10]
    context = {
        'home_sections': home_sections,
        'palaces': palaces,
        'whychoose': whychoose,
        'destinations':destinations,
        'hotels': hotels,
        'camps': camps,
        'activities': activities,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)





def About(request):
    about = AboutSection.objects.first()
    reviews = Review.objects.filter(approved=True).order_by('-created_at')[:10]
    context = {
        "about": about,
        'reviews': reviews,
    }
    return render(request,'about.html',context)




def Faq(request):
    return render(request,'faq.html')



def Contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully! We will get back to you within 24 hours.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})



def Terms(request):
    return render(request ,'terms.html')



def privercy(request):
    return render(request,'privercy.html')
