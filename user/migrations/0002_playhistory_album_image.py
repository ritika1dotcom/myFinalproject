# Generated by Django 4.2.5 on 2023-10-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playhistory',
            name='album_image',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]