from django.urls import path
from Adventure.views import Activity_Details_View,Activities , activity_booking_pending

urlpatterns = [
    path('adventure/',Activities , name= 'adventure'),
    path('adventure-details/<slug:slug>/', Activity_Details_View, name='activity_detail'),
    path('activity-booking/<str:booking_id>/pending/', activity_booking_pending, name='activity_booking_pending'),
]
