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

    # Add data to table

    # Print table

if __name__ == "__main__":
    main()
