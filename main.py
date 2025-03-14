import os
import asyncio
import aiohttp
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

HEADERS = {
    "referer": "https://skybars.me/",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

URL = "https://main.mcmcmc.net/utils/sb_online.json"
PLAYERS_FILE = "players.txt"
LOG_FILE = "log.txt"

async def fetch_players():
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        try:
            async with session.get(URL) as response:
                data = await response.text()
                start_idx = data.find('players":"') + 10
                end_idx = data.rfind('"')
                players = data[start_idx:end_idx].split(", ")
                return players
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            return []

async def save_new_players(players):
    if not os.path.exists(PLAYERS_FILE):
        open(PLAYERS_FILE, "w").close()
    
    with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
        existing_players = set(f.read().splitlines())
    
    new_players = [p for p in players if p not in existing_players]
    
    if new_players:
        with open(PLAYERS_FILE, "a", encoding="utf-8") as f:
            for player in new_players:
                f.write(player + "\n")
        log_event(new_players)
    await asyncio.sleep(3)
    return new_players


def log_event(players):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Added players: {', '.join(players)}\n"
    
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
    
    console.print(Text(log_entry, style="bold cyan"))


async def main():
    console.print("[bold green][+] Запуск программы...[/bold green]")
    while True:
        players = await fetch_players()
        if players:
            new_players = await save_new_players(players)
            
            table = Table(title="Обнаружены новые игроки", style="bold yellow")
            table.add_column("Игрок", style="bold white")
            
            for player in new_players:
                table.add_row(player)
            
            if new_players:
                console.print(table)
        
        await asyncio.sleep(30)

if __name__ == "__main__":
    asyncio.run(main())
