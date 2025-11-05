import requests

class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.nationality = dict['nationality']
        self.assists = dict['assists']
        self.goals = dict['goals']
        self.team = dict['team']
        self.games = dict['games']

    def get_goals_assists(self):
        return self.goals + self.assists
    
    def __str__(self):
        return f"{self.name:30}{self.team:20}{self.goals} + {self.assists} = {self.get_goals_assists()}"

class PlayerReader:
    def __init__(self, url):
        self.data = requests.get(url).json() # JSON-data
        self.players = list()

    def get_players(self):
        for player_dict in self.data:
            player = Player(player_dict)
            self.players.append(player)

        return self.players

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        self.grouped = list()
        for player in self.players:
            if player.nationality == nationality:
                self.grouped.append(player)

        return sorted(self.grouped, key=lambda player: player.get_goals_assists(), reverse=True)
