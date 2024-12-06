from django.db import models

# Create your models here.
class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('AUTO', 'Automatic'),
        ('MANUAL', 'Manual'),
    ]

    image = models.ImageField(upload_to='car_images/')
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    automation = models.CharField(max_length=10, choices=TRANSMISSION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Staff(models.Model):
    passportimage = models.ImageField(upload_to='staff_images/', blank=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    desgination = models.CharField(max_length=100)
    twitter_link = models.URLField(blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)


    def __str__(self):
        return f'{self.name} ({self.desgination})'
