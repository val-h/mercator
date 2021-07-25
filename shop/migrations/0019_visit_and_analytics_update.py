# Generated by Django 3.2.5 on 2021-07-25 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_sample_analytics_visit_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='shop_analytics',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='visits', to='shop.shopanalytics'),
        ),
    ]
