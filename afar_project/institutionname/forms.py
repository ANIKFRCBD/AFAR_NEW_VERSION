from django import forms
from django.core.validators import FileExtensionValidator

class institutionname_form(forms.Form):
    Name = forms.CharField(max_length=255)
    Website = forms.CharField(max_length=255)
    District = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    authority = forms.CharField(max_length=255)
    document = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
