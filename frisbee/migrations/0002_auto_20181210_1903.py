# Generated by Django 2.1.4 on 2018-12-10 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_full',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='game',
            name='game_type',
            field=models.IntegerField(default=4),
        ),
    ]
