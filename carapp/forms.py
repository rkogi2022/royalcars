from django import forms

from carapp.models import DriverApplication, CarBooking, CarPurchase, Newsletter

from carapp.models import ContactMessage


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

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control p-4', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control p-4', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control py-3 px-4', 'placeholder': 'Message', 'rows': 5}),
        }