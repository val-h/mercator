# Generated by Django 3.2.5 on 2021-07-24 01:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_review_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='customer',
        ),
    ]
