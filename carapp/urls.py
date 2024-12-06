from django.urls import path

from carapp import views

urlpatterns = [
    path('index/',views.index, name='index'),
    path('newsletter/', views.subscribe_newsletter, name='newsletter'),
    path('about/',views.about, name='about'),
    path('services/',views.services, name='services'),
    path('apply/', views.apply_as_driver, name='driver-apply'),
    path('book-car/<int:car_id>/', views.book_car, name='book_car'),
    path('book_road_test/<int:car_id>/', views.book_road_test, name='book_road_test'),
    path('mpesa-callback/', views.mpesa_callback, name='mpesa_callback'),
    path('cardetails/', views.cardetails, name='cardetails'),
    path('ridehail/<int:car_id>/', views.ridehail, name='ridehail'),
    path('team_view/', views.team_view, name='team_view'),
]