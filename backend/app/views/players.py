# -*- coding: utf-8 -*-
import logging
from functools import partial
import json
import os

from rest_framework.response import Response
from rest_framework.views import APIView, exception_handler
from app.dbmodels import models
from django.forms.models import model_to_dict

LOGGER = logging.getLogger('django')


class PlayerSummary(APIView):
    logger = LOGGER

    def snake_dict_key_to_camel(self, d):
        """Converts the keys of a dictionary from snake_case to camelCase.

        PreC: `d` is a dictionary where keys are in snake_case format.

        Args:
            d (dict): A dictionary with keys in snake_case format.

        Returns:
            dict: A new dictionary with all keys converted to camelCase.

        Example:
            Input: {"player_name": "Michael Jordan", "total_points": 30}
            Output: {"playerName": "Michael Jordan", "totalPoints": 30}
    """
        def snake_str_to_camel(s):
            return ''.join([s.title() if i != 0 else s for i, s in enumerate(s.split('_'))])

        return {snake_str_to_camel(k): v for k, v in d.items()}
    def get(self, request, playerID):
        """Handles GET requests to retrieve player summary data by player ID.

        PreC: `playerID` is a valid integer corresponding to an existing player in the database.

        Args:
            request (HttpRequest): The incoming HTTP GET request.
            playerID (int): The ID of the player for whom the data is being requested.

        Returns:
            Response: A JSON response containing the player's name and game statistics, 
            or an error response if something goes wrong (e.g., player not found)."""
        def player_stat_to_dict(player_stat):
            """Converts a PlayerStat instance into a dictionary, including game date and shot data.

            PreC: `player_stat` is a valid instance of the PlayerStat model, with a foreign key to a Game model and associated Shot data.

            Args:
            player_stat (PlayerStat): A PlayerStat model instance representing a player's performance in a particular game.

            Returns:
            dict: A dictionary representing the player's performance, including game date and a list of shots, with keys in camelCase."""

            game_id = player_stat.game_id
            player_stat_id = player_stat.id
            game = models.Game.objects.get(id=game_id)
            player_stat_dict = self.snake_dict_key_to_camel(model_to_dict(player_stat, exclude=['id', 'game', 'player', 'team']))
            shots = models.Shot.objects.filter(player_stat_id=player_stat_id)
            shot_list = [self.snake_dict_key_to_camel(model_to_dict(shot, exclude=['id', 'player_stat'])) for shot in shots] 
            player_stat_dict.update({'date': game.date, 'shots': shot_list})
            return player_stat_dict
        
        
        """
        Attempts to retrieve player data and associated game statistics based on the provided playerID.

        The code first tries to retrieve the player's details using the `Player` model by querying the database for a player with the given `playerID`. 
        If the player exists, it fetches the player's statistics from the `PlayerStat` model, processes the statistics for each game , 
        and stores them in the `result` dictionary. The games are then sorted by the game date, and the final result is returned as a JSON response.

        In the event of an exception (e.g., player not found, database error), the code catches the exception and 
        returns an error response with a status of "error" and a message indicating the reason for the failure.
        """
        try:
            result = {}
            player = models.Player.objects.get(id=playerID)
            result['name'] = player.name

            player_stats = models.PlayerStat.objects.filter(player_id=playerID)
            games = [player_stat_to_dict(player_stat) for player_stat in player_stats]
            games.sort(key=lambda x: x['date'])
            result['games'] = games
            
            return Response(result)
        
        except Exception as e:
            return Response({"status": "error", "reason": str(e)})

   
