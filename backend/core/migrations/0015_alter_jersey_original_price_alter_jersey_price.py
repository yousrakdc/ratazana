# Generated by Django 5.1.1 on 2024-10-04 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_jersey_original_price_jersey_sizes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jersey',
            name='original_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='jersey',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
