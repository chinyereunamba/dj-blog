# Generated by Django 4.2 on 2024-12-23 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_blogpost_publish_blogpost_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, verbose_name='Slug'),
        ),
    ]
