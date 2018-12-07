from django.db import models
import datetime
 # Create your models here.


class Game(models.Model):
  location = models.CharField(max_length=100)
  team1_score = models.IntegerField()
  team2_score = models.IntegerField()
  class Meta:
    db_table = "GameTable"
  
class Team(models.Model):
  team_name = models.CharField(max_length=100)
  win_count = models.IntegerField()
  loss_count = models.IntegerField()
  tie_count = models.IntegerField()
  class Meta:
    db_table = "TeamTable" 

class User(models.Model):
  password = models.CharField(max_length=128)
  email = models.CharField(max_length=30)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  is_leader = models.BooleanField(default=False)
  team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
  receive_reminder = models.BooleanField(default=False)
  class Meta:
    db_table = "UserTable"

class Event(models.Model):
  eventName = models.CharField(max_length=200, default="Placehold Name")
  location = models.CharField(max_length=200)
  date = models.DateField(default=datetime.date.today)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  class Meta:
    db_table = "EventTable"
