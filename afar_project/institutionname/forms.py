from django import forms
from django.core.validators import FileExtensionValidator

class institutionname_form(forms.Form):
    Name = forms.CharField(max_length=255)
    Abbreviation=forms.CharField(max_length=255)
    Website = forms.CharField(max_length=255)
    District = forms.CharField(max_length=255)
    street_address = forms.CharField(max_length=255)
    authority = forms.CharField(max_length=255)
    phone=forms.CharField(max_length=255)
    email=forms.EmailField(max_length=225)
    logo = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    
