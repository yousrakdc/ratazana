# Generated by Django 5.1.1 on 2024-10-01 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_jerseyimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jerseyimage',
            old_name='image',
            new_name='image_path',
        ),
    ]
