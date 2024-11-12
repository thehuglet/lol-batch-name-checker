import asyncio
from timeit import default_timer as timer
from pathlib import Path
from console_utils import draw, clearscreen, quickedit, TODAY_DATE
from league_api import get_server_name, check_name_change, check_new_summoner
from willump import Willump

NAME_LIST_FILENAME = 'names.txt'

def draw_full_header(server_name: str, date: str) -> None:
    """Draws the header with server and date info."""
    header = f"""
    ┌──────────────────────┐
    │   LoL-BNC by huglet  │
    ├───────┬──────────────┤
    │  {server_name:<4} │  {date}  │
    ├───┬───┴──────────────┼──────────────────┐
    │   │       Name       │     In Game      │
    ├───┼──────────────────┼──────────────────┤"""
    draw(header)

def simulate_in_game(name: str) -> str:
    """Replaces Greek characters with placeholders in the given name."""
    box_greek_letters = 'ΑΒΕΖΗΙΚΜΝΟΡΤΥΧ'
    for letter in box_greek_letters:
        name = name.replace(letter, '□')
    return name

async def main() -> None:
    """Main control flow for JanitorBot."""
    quickedit(False)  # Disable quick edit mode
    wllp = await Willump.start()
    start_time = timer()
    found, total = 0, 0
    
    server_name = await get_server_name(wllp)
    clearscreen()
    draw_full_header(server_name, TODAY_DATE)
    
    async with Path(NAME_LIST_FILENAME).open("r", encoding="utf8") as names_file:
        async for name in names_file:
            name = name.strip()
            if 3 <= len(name) <= 16:
                total += 1
                if await check_name_change(wllp, name):
                    found += 1
                    nc_only = '*' if not await check_new_summoner(wllp, name) else ' '
                    draw(f'    │ {nc_only} │ {name:<16} │ {simulate_in_game(name):<16} │')

    duration = round(timer() - start_time, 2)
    draw(f"\nChecked {total} names in {duration} seconds. Found {found} available names.\n")
    await wllp.stop()

if __name__ == '__main__':
    asyncio.run(main())
