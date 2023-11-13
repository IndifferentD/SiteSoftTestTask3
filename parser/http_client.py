from aiohttp import ClientSession


async def fetch_html(session: ClientSession, url: str):
    async with session.get(url) as response:
        return url, await response.text()
