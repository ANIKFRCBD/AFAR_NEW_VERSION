from django import forms

class deletedata(forms.Form):
    asset_code=forms.CharField(max_length=128,required=False)