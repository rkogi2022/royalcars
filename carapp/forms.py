from django import forms

from carapp.models import DriverApplication, CarBooking, CarPurchase, Newsletter


class DriverApplicationForm(forms.ModelForm):
    class Meta:
        model = DriverApplication
        fields = ['first_name', 'last_name', 'age', 'gender', 'county', 'driving_class']
        widgets = {
            'gender': forms.Select(),  # No need to redefine choices
            'driving_class': forms.Select(),
        }
class BookCarForm(forms.ModelForm):
    class Meta:
        model = CarBooking
        fields = ['name', 'phone_number', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CarPurchaseForm(forms.ModelForm):
    class Meta:
        model = CarPurchase
        fields = ['customer_name', 'phone_number', 'id_number', 'kra_pin', 'road_test_date']
        widgets = {
            'road_test_date': forms.DateInput(attrs={'type': 'date'}),
        }
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']
