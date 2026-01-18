from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('edit/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
]
