# Generated by Django 3.2.6 on 2021-08-06 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_visit_and_analytics_update'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-date_created']},
        ),
        migrations.RemoveField(
            model_name='product',
            name='total_views',
        ),
        migrations.AlterField(
            model_name='shopstyle',
            name='background_image',
            field=models.ImageField(blank=True, default=None, upload_to='images/shops/'),
        ),
        migrations.AlterField(
            model_name='shopstyle',
            name='logo',
            field=models.ImageField(blank=True, default='images/shops/shop_default_logo.png', upload_to='images/shops/'),
        ),
    ]
