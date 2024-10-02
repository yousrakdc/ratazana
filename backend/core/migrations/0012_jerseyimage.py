# Generated by Django 5.1.1 on 2024-10-01 17:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_image_jersey_image_path'),
    ]

    operations = [
        migrations.CreateModel(
            name='JerseyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='jerseys/')),
                ('jersey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='core.jersey')),
            ],
        ),
    ]