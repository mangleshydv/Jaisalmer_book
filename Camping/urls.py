from django.urls import path
from Camping.views import Camping,Camping_Details,camp_booking_pending


urlpatterns = [
    path('Camping-Tent/',Camping,name='camp_list'),
    path('camp_details/<slug:slug>/', Camping_Details, name='camp_detail'),
     path('Camp_booking_pending/<str:booking_id>/', camp_booking_pending, name='camp_booking_pending'),
]
