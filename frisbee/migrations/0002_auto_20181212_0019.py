# Generated by Django 2.1.4 on 2018-12-12 00:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('frisbee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='name',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='team_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_1', to='frisbee.Team'),
        ),
        migrations.AlterField(
            model_name='game',
            name='team_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_2', to='frisbee.Team'),
        ),
        migrations.AlterField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='frisbee.Team'),
        ),
    ]