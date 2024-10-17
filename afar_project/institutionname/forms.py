from django import forms

class institutionname_form(forms.Form):
    Name = forms.CharField(max_length=255)
    Website = forms.URLField()
    District = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    authority = forms.CharField(max_length=255)
    document = forms.FileField()
