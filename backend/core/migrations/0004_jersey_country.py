# Generated by Django 5.1.1 on 2024-09-27 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_jersey_description_jersey_is_new_release_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jersey',
            name='country',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]
