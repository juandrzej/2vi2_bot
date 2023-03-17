from datetime import datetime
from enum import Enum
from typing import List


class Player:
    def __init__(self, discord_id, nickname):
        self.nickname = nickname
        self.discordId = discord_id
        self.civilization = None

    def set_civilization(self, civilization):
        self.civilization = civilization


class TeamGameStatus(Enum):
    LOST = 0,
    WON = 1


class Team:
    def __init__(self, team_name, players, banned_civilizations, team_game_status):
        self.teamName = team_name
        self.teamGameStatus = team_game_status
        self.users = players
        self.bannedCivilizations = banned_civilizations


class Game:
    def __init__(self, game_date, tournament_name, teams):
        self.teams = teams
        self.gameDate = game_date
        self.tournamentName = tournament_name

    teams: List[Team]
    gameDate: datetime
    tournamentName: str
