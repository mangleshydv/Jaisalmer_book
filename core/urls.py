from django.urls import path
from core.views import Home_View,About,Faq,Contact,Terms,privercy


urlpatterns = [
    path('',Home_View,name='home'),
    path('about-us/',About , name='about'),
    path('Faq/',Faq , name='faq'),
    path('contact-us/',Contact , name='contact'),
    path('Terms-&-Condition/',Terms , name='Terms'),
    path('Privacy-Policy/',privercy , name='Privacy'),
]
