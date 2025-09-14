from django.urls import path
from Hotel.views import Hotels_View,hotel_detail_view,booking_pending

urlpatterns = [
    path('Hotels/', Hotels_View ,name='hotel'),
    path('hotel/<slug:slug>/', hotel_detail_view, name='hotel_detail'),
    path('booking/pending/<str:booking_id>/', booking_pending, name='booking_pending'),
]
