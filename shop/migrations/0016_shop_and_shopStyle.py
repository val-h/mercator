# Generated by Django 3.2.5 on 2021-07-24 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0015_updated_shipment_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(default='images/shops/shop_default_logo.png', upload_to='images/shops/')),
                ('background_style', models.CharField(choices=[('C', 'Color'), ('I', 'Image')], default='C', max_length=3)),
                ('first_theme_color', models.CharField(default='#f8f9fa', max_length=7)),
                ('second_theme_color', models.CharField(default='#f6bd60', max_length=7)),
                ('third_theme_color', models.CharField(default='#343a40', max_length=7)),
                ('background_color', models.CharField(default='#000000', max_length=7)),
                ('background_image', models.ImageField(default=None, upload_to='images/shops/')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('points', models.IntegerField()),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='shop', to=settings.AUTH_USER_MODEL)),
                ('style', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop.shopstyle')),
            ],
        ),
    ]
