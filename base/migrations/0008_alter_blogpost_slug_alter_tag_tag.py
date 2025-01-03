# Generated by Django 5.1.4 on 2024-12-24 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_account_email_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(max_length=50, unique=True, verbose_name='Tag'),
        ),
    ]
