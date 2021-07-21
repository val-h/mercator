# Generated by Django 3.2.5 on 2021-07-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_order_items'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=80)),
                ('last_name', models.CharField(max_length=80)),
                ('company', models.CharField(blank=True, max_length=120)),
                ('address', models.CharField(max_length=120)),
                ('post_code', models.CharField(max_length=120)),
                ('state', models.CharField(max_length=80)),
                ('city', models.CharField(max_length=120)),
                ('contact_number', models.CharField(max_length=20)),
                ('shipping_method', models.CharField(choices=[('ML', 'Mail'), ('PD', 'Parcel Delivery Company'), ('JB', 'Jeff Bezos with a bycicle (cheapest)')], default='ML', max_length=2)),
            ],
        ),
    ]
