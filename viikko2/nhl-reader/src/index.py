from player import PlayerReader, PlayerStats
from rich.console import Console
from rich.table import Table
from rich.theme import Theme

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    # Rich console with colors as theme:
    my_theme = Theme({
        "header": "bold cyan",
        "player": "magenta",
        "team": "green",
        "stats": "yellow",
        "error": "bold red",
    })
    console = Console(theme=my_theme)

    # Get nationalities for display at user input:
    nationalities = reader.get_nationality_string()

    # User input
    while True:
        input = console.input(f"Select natinoality: [magenta]{nationalities}[/magenta]\nor type exit to quit: ").upper()

        if input == "exit".upper():
            break

        players = stats.top_scorers_by_nationality(input)

        if not players:
            console.print(f"[error]No players of nationality [magenta]{input}[/magenta] found![/error]")

    # Create table
        table = Table(title=f"NHL players from ({input})", style="bold white")
        table.add_column("Name", justify="left", style="player", no_wrap=True)
        table.add_column("Team", justify="center", style="team")
        table.add_column("Goals", justify="center", style="stats")
        table.add_column("Assists", justify="center", style="stats")
        table.add_column("Points", justify="center", style="bold yellow")

    # Add data to table
        for player in players:
            table.add_row(
                player.name,
                player.team,
                str(player.goals),
                str(player.assists),
                str(player.get_goals_assists())
            )

    # Print table
        console.print()
        console.print(table)

if __name__ == "__main__":
    main()
