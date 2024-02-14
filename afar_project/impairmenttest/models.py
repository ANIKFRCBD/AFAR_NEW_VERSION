from django.db import models

# Create your models here.
class impairmententry_model(models.Model):
    Value_in_use=models.FloatField(null=True)
    Fair_value_less_cost_to_sale=models.FloatField(null=True)
    Asset_Code=models.CharField(null=False)
    Financial_year=models.CharField(null=False)
class entryfinderm(models.Model):
    Asset_Code=models.CharField(null=False)