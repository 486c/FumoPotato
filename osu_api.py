from __future__ import annotations
from typing import Optional

from aiohttp import ClientSession

import settings

class osuAPI:
    def __init__(self) -> None:
        self.session = ClientSession()

    async def get_beatmaps(self, bid: int) -> Optional[dict]:
        link = (
            "https://osu.ppy.sh/api/get_beatmaps"
            f"?k={settings.OSU_API_KEY}"
            f"&b={bid}"
        )

        r = await self.session.get(link)

        if r.status != 200:
            return None

        j = await r.json()
        if len(j) == 1:
            return j[0]
        else:
            return j

    async def get(self, url: str):
        r = await self.session.get(url)
        return r

    async def close(self) -> None:
        await self.session.close()
