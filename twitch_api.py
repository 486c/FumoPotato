from aiohttp import ClientSession

import settings

from typing import Optional

class twitchAPI:
    def __init__(self) -> None:
        self.session = ClientSession()

    async def get_stream(self, username: str) -> Optional[dict]:
        link = (
            "https://api.twitch.tv/helix/streams"
            f"?user_login={username}"
        )

        headers = {
            'Client-Id': settings.TWITCH_CLIENT_ID,
            'Authorization': f'Bearer {settings.TWITCH_KEY}',
        }

        r = await self.session.get(link, headers=headers)

        if r.status != 200:
            return None

        j = await r.json()
        if j['data'] == []:
            return None
        else:
            return j['data'][0]

    async def close(self) -> None:
        await self.session.close()
