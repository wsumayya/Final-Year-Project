# Generated by Django 4.2.3 on 2025-01-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nutri', '0003_remove_meal_price_meal_calories'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='meal_images/'),
        ),
    ]
