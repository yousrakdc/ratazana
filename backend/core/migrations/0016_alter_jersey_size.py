# Generated by Django 5.1.1 on 2024-10-04 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_alter_jersey_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jersey',
            name='size',
            field=models.CharField(default='N/A', max_length=50),
        ),
    ]
