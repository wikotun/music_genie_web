# Generated by Django 4.1.1 on 2022-11-12 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0004_remove_artist_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='release_date',
            field=models.DateField(null=True),
        ),
    ]
