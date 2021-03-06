# Generated by Django 2.1.4 on 2018-12-11 22:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventName', models.CharField(default='Placehold Name', max_length=200)),
                ('location', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
                ('is_full', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'EventTable',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('team1_score', models.IntegerField()),
                ('team2_score', models.IntegerField()),
                ('field_num', models.IntegerField()),
                ('game_type', models.IntegerField(default=4)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frisbee.Event')),
            ],
            options={
                'db_table': 'GameTable',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=100)),
                ('win_count', models.IntegerField()),
                ('loss_count', models.IntegerField()),
                ('tie_count', models.IntegerField()),
            ],
            options={
                'db_table': 'TeamTable',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('email', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('is_leader', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('receive_reminder', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(auto_now_add=True)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frisbee.Team')),
            ],
            options={
                'db_table': 'UserTable',
            },
        ),
        migrations.AddField(
            model_name='game',
            name='team_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_1', to='frisbee.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='team_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_2', to='frisbee.Team'),
        ),
        migrations.AddField(
            model_name='event',
            name='teams',
            field=models.ManyToManyField(to='frisbee.Team'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frisbee.User'),
        ),
    ]
