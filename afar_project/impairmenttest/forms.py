from django.forms import ModelForm
from .models import impairmententry_model

class impairmententry(ModelForm):
    class Meta:
        model = impairmententry_model
        fields = ["Value_in_use", "Fair_value_less_cost_to_sale"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Value_in_use"].required = False
        self.fields["Fair_value_less_cost_to_sale"].required = False
