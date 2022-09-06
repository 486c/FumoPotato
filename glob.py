from __future__ import annotations

from osu_api import osuAPI
from twitch_api import twitchAPI
from motor.motor_asyncio import AsyncIOMotorDatabase

__all__ = ("osu", "mongo", "twitch")

osu: osuAPI
twitch: twitchAPI
mongo: AsyncIOMotorDatabase
