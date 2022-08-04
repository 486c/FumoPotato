from __future__ import annotations

from aiohttp import ClientSession

class osuAPI:
    def __init__(self) -> None:
        self.session = ClientSession()

    async def close(self) -> None:
        await self.session.close()
