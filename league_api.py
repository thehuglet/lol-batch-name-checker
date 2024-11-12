from willump import Willump
import asyncio

async def get_server_name(wllp: Willump) -> str:
    """Fetches server name for current session."""
    response = await wllp.request('get', '/lol-store/v1/getStoreUrl')
    store_url = await response.json()
    return store_url[8:-26].upper()

async def check_name_change(wllp: Willump, name: str) -> bool:
    """Checks if a name change is available for a given summoner name."""
    response = await wllp.request('get', f'/lol-summoner/v1/check-name-availability/{name}')
    return await response.json()

async def check_new_summoner(wllp: Willump, name: str) -> bool:
    """Checks if a new summoner can use the provided name."""
    response = await wllp.request('get', f'/lol-summoner/v1/check-name-availability-new-summoners/{name}')
    return await response.json()
