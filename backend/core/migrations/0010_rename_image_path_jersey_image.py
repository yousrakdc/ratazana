# Generated by Django 5.1.1 on 2024-10-01 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_jersey_image_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jersey',
            old_name='image_path',
            new_name='image',
        ),
    ]