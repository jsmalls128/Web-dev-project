# Generated by Django 2.1.4 on 2018-12-07 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee', '0002_auto_20181205_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frisbee.Team'),
        ),
    ]
