from django.forms import ModelForm
from django import forms
from .models import sales_entry_model,entryfinder_sales

class sales_entry_form(ModelForm):
    class Meta:
        model = sales_entry_model
        fields = ["Asset_code","Number","Sales_proceeds","Financial_year","Year_elapsed"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Asset_code"].required = False
        self.fields["Number"].required = False
        self.fields["Sales_proceeds"].required = False
        self.fields["Financial_year"].required=False
        self.fields["Year_elapsed"].required=False
class entryfinder_sales(ModelForm):
    class Meta:
        model = entryfinder_sales # replace with your model
        fields = ['Asset_Code']  # corrected typo 'fields'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Asset_Code"].required = False