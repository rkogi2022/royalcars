from django import forms

from dashboard.models import Car, Staff


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['image', 'name', 'year', 'automation', 'price', 'rental_price']

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['passportimage', 'name', 'age', 'gender', 'desgination','twitter_link','facebook_link','linkedin_link']
        widgets = {
            'passportimage': forms.ClearableFileInput(
                attrs={'class': 'form-control', 'accept': 'image/*', 'title': 'Upload Passport Image Here'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter age'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your gender'}),
            'desgination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your desgination'}),
            'twitter_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your twitter link'}),
            'facebook_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your facebook link'}),
            'linkedin_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your linkedin link'}),
        }