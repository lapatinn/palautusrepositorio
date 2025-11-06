from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from player import PlayerReader, PlayerStats

def init_console():
    # Rich console with colors as theme:
    my_theme = Theme({
        "header": "bold cyan",
        "player": "magenta",
        "team": "green",
        "stats": "yellow",
        "error": "bold red",
    })

    console = Console(theme=my_theme)
    return console

def init_reader():
    reader = PlayerReader("https://studies.cs.helsinki.fi/nhlstats/2024-25/players")
    stats = PlayerStats(reader)

    return reader, stats

def create_table(user_input):
    # Create table
    table = Table(title=f"NHL players from ({user_input})", style="bold white")
    table.add_column("Name", justify="left", style="player", no_wrap=True)
    table.add_column("Team", justify="center", style="team")
    table.add_column("Goals", justify="center", style="stats")
    table.add_column("Assists", justify="center", style="stats")
    table.add_column("Points", justify="center", style="bold yellow")

    return table

def populate_table(players, table):
    # Add data to table
    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.get_goals_assists())
        )

def print_table(console, players, table):
    # Print table
    console.print()
    # Only print if players found
    if players:
        console.print(table)


def main():
    # Initialize components
    reader, stats = init_reader()
    console = init_console()

    # Get nationalities for display at user input:
    nationalities = reader.get_nationality_string()

    # Most disgusting, least readable while-loop I've ever made:
    # Handle user input, construct and print table:
    while True:
        user_input = console.input(f"""Select natinoality: [magenta]{nationalities}[/magenta]
or type exit to quit: """).upper()

        # Exit code:
        if user_input == "exit".upper():
            break

        # Nice purple string with nationalities in alphapetical order :3
        players = stats.top_scorers_by_nationality(user_input)

        # Don't print table if no players found
        if not players:
            console.print(f"""
[error]No players of nationality [magenta]{user_input}[/magenta] found![/error]""")

        # Create, populate and print table
        table = create_table(user_input)
        populate_table(players, table)
        print_table(console, players, table)

if __name__ == "__main__":
    main()
