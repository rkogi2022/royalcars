from django.db import models

from datetime import date
from decimal import Decimal

from dashboard.models import Car
# Create your models here.


class DriverApplication(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    DRIVING_CLASS_CHOICES = [
        ('B1', 'B1'),
        ('B2', 'B2'),
        ('C1', 'C1'),
        ('C2', 'C2'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    county = models.CharField(max_length=100)
    driving_class = models.CharField(max_length=2, choices=DRIVING_CLASS_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class CarBooking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, default=None)
    phone_number = models.CharField(max_length=15, default=None)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='Pending')
    transaction_time = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        days_booked = (self.end_date - self.start_date).days
        self.total_amount = self.car.rental_price * days_booked  # Calculate total
        self.deposit = self.total_amount * Decimal('0.5')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.car.name} Booking"

class CarPurchase(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='purchases')
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    id_number = models.CharField(max_length=20)
    kra_pin = models.CharField(max_length=20)
    road_test_date = models.DateField()
    road_test_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name} - {self.car.name}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

class RideHailing(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pickup_location = models.CharField(max_length=255)
    pickup_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_location = models.CharField(max_length=255)
    dropoff_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    dropoff_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pickup_date = models.DateField()
    pickup_time = models.TimeField()

    def __str__(self):
        return f"Booking for {self.car.name}"