from django.db import models

# Create your models here.
class User(models.Model):
  password = models.CharField(max_length=128)
  email = models.CharField(max_length=30)
  first_name = models.CharField(max_length=30)
  last_name = models.CharField(max_length=30)
  is_leader = models.BooleanField(default=False)
  receive_reminder = models.BooleanField(default=False)
  class Meta:
    db_table = "UserTable"
      
class Event(models.Model):
  location = models.CharField(max_length=100)
  class Meta:
    db_table = "EventTable"
  
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