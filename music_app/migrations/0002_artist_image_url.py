# Generated by Django 4.1.1 on 2022-11-09 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='image_url',
            field=models.CharField(max_length=200, null=True),
        ),
    ]