from django.urls import path

from dashboard import views

urlpatterns = [
    path('car_list/', views.car_list, name='car_list'),
    path('car/new/', views.car_create, name='car_create'),
    path('car/edit/<int:pk>/', views.car_edit, name='car_edit'),
    path('car/delete/<int:pk>/', views.car_delete, name='car_delete'),
    path('driver-applications/', views.driver_applications, name='driver_applications'),
    path('application/edit/<int:pk>/', views.edit_application, name='edit_application'),
    path('car-bookings/', views.car_bookings, name='car_bookings'),
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('newsletter/', views.newsletter_list, name='newsletter_list'),
    path('ride-hailing/', views.ride_hailing_list, name='ride_hailing_list'),
    path('staff/', views.staff_list, name='staff_list'),
    path('add/', views.add_staff, name='add_staff'),
    path('edit/<int:pk>/', views.edit_staff, name='edit_staff'),
    path('delete/<int:pk>/', views.delete_staff, name='delete_staff')
]