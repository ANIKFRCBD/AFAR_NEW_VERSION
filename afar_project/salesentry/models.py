from django.db import models


# Create your models here.
class sales_entry_model(models.Model):
    Asset_code=models.CharField(null=True)
    Number=models.IntegerField(null=True)
    Sales_proceeds=models.FloatField(null=True)
    Financial_year=models.CharField(null=True)
    Year_elapsed=models.IntegerField(null=True)
class entryfinder_sales(models.Model):
    Asset_Code=models.CharField(null=False)


