# Generated by Django 4.2 on 2024-12-23 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_blogpost_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]