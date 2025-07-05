import json
from django.core.management.base import BaseCommand
from pathlib import Path
from app.dbmodels.models import Team, Player, Game, PlayerStat, Shot
from datetime import datetime

# Set the base directory of the project to access the JSON files
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Command(BaseCommand):
    """
    Custom Django management command to load data from JSON files into the database.
    The process uses get_or_create to ensure records are not duplicated when the command is run multiple times.
    """

    JSON_FILE_DIRECTORY = 'raw_data'
    TEAMS_JSON_FILE = 'teams.json'
    GAMES_JSON_FILE = 'games.json'
    PLAYERS_JSON_FILE = 'players.json'

    help = 'Load data from JSON files into the PostgreSQL database.'

    def handle(self, *args, **kwargs):
        """
        Main entry point for the management command. This method coordinates the loading
        of teams, players, and games from their respective JSON files into the database.
        """
        self.handle_teams_file()
        self.handle_players_file()
        self.handle_games_file()

    def handle_teams_file(self):
        """
        Loads team data from the teams.json file into the Team model.
        Uses get_or_create to avoid duplicating data if the command is run multiple times.
        """
        with open(BASE_DIR / self.JSON_FILE_DIRECTORY / self.TEAMS_JSON_FILE, encoding='utf-8') as file:
            teams = json.load(file)

        for team in teams:
            try:
                Team.objects.create(id=team['id'], name=team['name'])
            except Exception as e:
                pass

    def handle_players_file(self):
        """
        Loads player data from the players.json file into the Player model.
        Uses get_or_create to avoid duplicating data if the command is run multiple times.
        """
        with open(BASE_DIR / self.JSON_FILE_DIRECTORY / self.PLAYERS_JSON_FILE, encoding='utf-8') as file:
            players = json.load(file)

        for player in players:
            try:
                Player.objects.create(id=player['id'], name=player['name'])
            except Exception as e:
                pass

    def handle_games_file(self):
        """
        Loads game data from the games.json file into the Game, PlayerStat, and Shot models.
        Uses get_or_create for the game and players, and create for the shots (as shots are unique per game).
        """
        with open(BASE_DIR / self.JSON_FILE_DIRECTORY / self.GAMES_JSON_FILE, encoding='utf-8') as file:
            games = json.load(file)

        for game in games:
            try:
                away_team = game['awayTeam']
                home_team = game['homeTeam']
                date = datetime.strptime(game['date'], '%Y-%m-%d').date()
                game_id = game['id']

                # Create the game record, using get_or_create to prevent duplicates
                Game.objects.create(id=game_id, date=date, away_team_id=away_team['id'], home_team_id=home_team['id'])

                # Process both team player stats and create relevant records
                for team_stat in [away_team, home_team]:
                    team_id = team_stat['id']
                    for player_stat in team_stat['players']:
                        player_stat_dict = self.dict_camel_key_to_snake(player_stat)
                        player_id = player_stat_dict.pop('id')
                        shots = player_stat_dict.pop('shots')
                        player_stat_dict.update({'game_id': game_id, 'team_id': team_id, 'player_id': player_id})
                        player_stat_obj = PlayerStat.objects.create(**player_stat_dict)

                        player_stat_id = player_stat_obj.id
                        for shot in shots:
                            shot_dict = self.dict_camel_key_to_snake(shot)
                            shot_dict.update({'player_stat_id': player_stat_id})
                            Shot.objects.create(**shot_dict)

            except Exception as e:
                pass

    def dict_camel_key_to_snake(self, d):
        """
        Converts dictionary keys from camelCase to snake_case.
        
        Args:
            d (dict): A dictionary with keys in camelCase.

        Returns:
            dict: A new dictionary with keys converted to snake_case.
        """
        return {self.camel_str_to_snake(k): v for k, v in d.items()}

    def camel_str_to_snake(self, s):
        """
        Converts a single camelCase string to snake_case.
        
        Args:
            s (str): A string in camelCase format.

        Returns:
            str: The string converted to snake_case format.
        """
        return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')
