# -*- coding: utf-8 -*-
"""Contains models related to stats"""
from django.db import models
from datetime import date


class Team(models.Model):
    """
    Represents a team in the system.

    Fields:
        id (int): The primary key for the team.
        name (str): The name of the team, with a maximum length of 45 characters.
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'team'


class Player(models.Model):
    """
    Represents a player in the system.

    Fields:
        id (int): The primary key for the player.
        name (str): The name of the player, with a maximum length of 45 characters.
    """
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'player'


class Game(models.Model):
    """
    Represents a game between two teams.

    Fields:
        id (int): The primary key for the game.
        date (date): The date of the game. Defaults to today’s date.
        away_team (ForeignKey): A reference to the team playing as the away team.
        home_team (ForeignKey): A reference to the team playing as the home team.
    """
    id = models.IntegerField(primary_key=True)
    date = models.DateField(default=date.today)
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_teams')
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_teams')

    class Meta:
        db_table = 'game'


class PlayerStat(models.Model):
    """
    Represents a player's statistics for a specific game.

    Fields:
        id (AutoField): The primary key for player statistics.
        player (ForeignKey): A reference to the player.
        game (ForeignKey): A reference to the game.
        team (ForeignKey): A reference to the team the player belongs to in that game.
        Various fields to store the player’s performance statistics like assists, points, rebounds, etc.
    """
    date = models.DateField(default=date.today)
    id = models.AutoField(primary_key=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_starter = models.BooleanField(default=False)
    minutes = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    assists = models.PositiveSmallIntegerField(default=0)
    offensive_rebounds = models.PositiveSmallIntegerField(default=0)
    defensive_rebounds = models.PositiveSmallIntegerField(default=0)
    steals = models.PositiveSmallIntegerField(default=0)
    blocks = models.PositiveSmallIntegerField(default=0)
    turnovers = models.PositiveSmallIntegerField(default=0)
    defensive_fouls = models.PositiveSmallIntegerField(default=0)
    offensive_fouls = models.PositiveSmallIntegerField(default=0)
    free_throws_made = models.PositiveSmallIntegerField(default=0)
    free_throws_attempted = models.PositiveSmallIntegerField(default=0)
    two_pointers_made = models.PositiveSmallIntegerField(default=0)
    two_pointers_attempted = models.PositiveSmallIntegerField(default=0)
    three_pointers_made = models.PositiveSmallIntegerField(default=0)
    three_pointers_attempted = models.PositiveSmallIntegerField(default=0)
    

    

    class Meta:
        db_table = 'player_stat'


class Shot(models.Model):
    """
    Represents a shot taken by a player during a game.

    Fields:
        id (AutoField): The primary key for the shot.
        is_make (bool): Whether the shot was made or missed.
        location_x (DecimalField): The X-coordinate location of the shot on the court.
        location_y (DecimalField): The Y-coordinate location of the shot on the court.
        player_stat (ForeignKey): A reference to the player's performance stats in that game.
    """
    id = models.AutoField(primary_key=True)
    is_make = models.BooleanField(default=False)
    location_x = models.DecimalField(max_digits=3, decimal_places=1)
    location_y = models.DecimalField(max_digits=3, decimal_places=1)
    player_stat = models.ForeignKey(PlayerStat, on_delete=models.CASCADE, related_name='shots')

    class Meta:
        db_table = 'shot'