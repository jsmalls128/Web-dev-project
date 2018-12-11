from django.db import models
import datetime
 # Create your models here.
  
class Team(models.Model):
  team_name = models.CharField(max_length=100)
  win_count = models.IntegerField()
  loss_count = models.IntegerField()
  tie_count = models.IntegerField()
  
  def __str__(self):
    return self.team_name

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
  is_full = models.BooleanField(default=False)
  teams = models.ManyToManyField(Team)
  
  def __str__(self):
    return self.eventName

  class Meta:
    db_table = "EventTable"

class Game(models.Model):
  location = models.CharField(max_length=100)
  team1_score = models.IntegerField()
  team2_score = models.IntegerField()
  field_num = models.IntegerField()
  game_type = models.IntegerField(default=4)
  team_1 = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="team_1")
  team_2 = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name="team_2")
  event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
  
  def __str__(self):
    return self.team_1 + ' vs ' + self.team_2
  
  def whoWon(self):
    if self.team1_score > self.team2_score:
      return self.team_1
    elif self.team1_score < self.team2_score:
      return self.team_2
    else:
      return 'Tie'

  class Meta:
    db_table = "GameTable"
