# Generated by Django 4.1.7 on 2023-04-27 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('afar_app', '0007_input_field_extra_field_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='input_field',
            name='extra_field_number',
        ),
    ]
