import json
from datetime import datetime
from enum import Enum

import requests

from game import Player, Team, Game


class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, Enum):
            return obj.name
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, Player):
            return obj.__dict__
        elif isinstance(obj, Game):
            return obj.__dict__
        elif isinstance(obj, Team):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class GameAPI:
    def __init__(self, api_key, dev_mode=False):
        self.api_key = api_key
        self.base_url = "https://civplays-dev-main.azurewebsites.net/api/" if dev_mode else "https://civplays-prod-main.azurewebsites.net/api/"

    def create_game(self, game):
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}
        data = json.dumps(game, cls=GameEncoder)
        response = requests.post(self.base_url + 'discord/game/create', headers=headers, data=data)
        response.raise_for_status()
        return response.json()
