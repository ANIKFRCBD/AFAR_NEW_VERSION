from django.forms import ModelForm
from django import forms
from .models import impairmententry_model,entryfinderm

class impairmententry(ModelForm):
    class Meta:
        model = impairmententry_model
        fields = ["Value_in_use", "Fair_value_less_cost_to_sale","Asset_Code","Financial_year"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Value_in_use"].required = False
        self.fields["Fair_value_less_cost_to_sale"].required = False
        self.fields["Asset_Code"].required = False
        self.fields["Financial_year"].required=False

class entryfinder(ModelForm):
    class Meta:
        model = entryfinderm  # replace with your model
        fields = ['Asset_Code']  # corrected typo 'fields'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Asset_Code"].required = False
