# Generated by Django 5.1.4 on 2024-12-26 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_blogpost_publish_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='image',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to='profile/', verbose_name='Profile Image'),
        ),
    ]