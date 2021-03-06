# Generated by Django 3.2.6 on 2021-08-20 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_updated_models_on_delete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PL', 'Active'), ('CA', 'Canceled'), ('PR', 'Processing'), ('CO', 'Complete'), ('DE', 'Delivered')], default='PL', max_length=2),
        ),
    ]
