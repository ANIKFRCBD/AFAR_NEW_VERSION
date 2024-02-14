from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.db import models

# Create your models here.

from django.db import models

class input_field(models.Model):
    # financial_year = models.CharField(max_length=250)
    purchase_date = models.DateField()
    serial_no = models.IntegerField()
    bill_no = models.IntegerField()
    # economic_code = models.IntegerField()
    category = models.CharField(max_length=255)
    name_of_item = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    price = models.DecimalField(default=0.0, max_digits=20, decimal_places=5)
    Salvage_Value = models.IntegerField()
    # deprication_rate = models.DecimalField(default=0.0, max_digits=20, decimal_places=5)
    # asset_code = models.CharField(max_length=255)
    # expected_life = models.IntegerField()
    # depriciation_method = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    current_condition = models.CharField(max_length=255)

class depriciation_field(models.Model):
    financial_year = models.CharField(max_length=250)
    purchase_date = models.DateField()
    serial_no = models.IntegerField()
    bill_no = models.IntegerField()
    economic_code = models.IntegerField()
    category = models.CharField(max_length=255)
    name_of_item = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    price = models.IntegerField()
    sold_quantity = models.IntegerField()
    costs_of_asset_sold = models.DecimalField(default=0.0, max_digits=20, decimal_places=5)
    current_balance = models.DecimalField(default=0.0, max_digits=20, decimal_places=5)
    year_elapsed = models.IntegerField()
    asset_code_generated = models.CharField(max_length=255)
    asset_code = models.CharField(max_length=255)
    expected_life = models.IntegerField()
    depriciation_method = models.CharField(max_length=255)
    deprication_rate = models.DecimalField(default=0.0, max_digits=20, decimal_places=5)
    location = models.CharField(max_length=255)
    current_condition = models.CharField(max_length=255)
    accumulated_depriciation_for_sold_items = models.DecimalField(default=0.0, max_digits=20, decimal_places=5)
    net_accumulated_depricaition = models.DecimalField(default=0.0, max_digits=20, decimal_places=5)

class model_asset_info(models.Model):
    category = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    economic_code = models.CharField(max_length=100)
    expected_life_pre = models.IntegerField()
    expected_life_post = models.IntegerField()
    depreciation_method = models.CharField(max_length=100)