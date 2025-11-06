import requests

class Player:
    def __init__(self, player_dict):
        self.name = player_dict['name']
        self.nationality = player_dict['nationality']
        self.assists = player_dict['assists']
        self.goals = player_dict['goals']
        self.team = player_dict['team']
        self.games = player_dict['games']

    def get_goals_assists(self):
        return self.goals + self.assists

    def __str__(self):
        string = (
            f"{self.name:30}{self.team:20}{self.goals} + {self.assists}"
            f" = {self.get_goals_assists()}"
        )

        return string

class PlayerReader:
    def __init__(self, url):
        self.data = requests.get(url, timeout=10).json() # JSON-data
        self.players = []

    def get_players(self):
        for player_dict in self.data:
            player = Player(player_dict)
            self.players.append(player)

        return self.players

    def get_nationalities(self):
        nationalities_set = set()
        for player_dict in self.data:
            nationality = player_dict['nationality']
            nationalities_set.add(nationality)

        return sorted(list(nationalities_set))

    def get_nationality_string(self):
        nationalities = self.get_nationalities()
        nat_str = "/".join(nationalities)
        return f"[{nat_str}]"

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality):
        grouped = []
        for player in self.players:
            if player.nationality == nationality:
                grouped.append(player)

        return sorted(grouped, key=lambda player: player.get_goals_assists(), reverse=True)
