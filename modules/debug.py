from __future__ import annotations

from typing import Optional

import lightbulb
from lightbulb import PrefixCommand, SlashCommand

import time

import glob
import settings

plugin = lightbulb.Plugin("debug")

@plugin.command()
@lightbulb.command("ping", "See if bot alive")
@lightbulb.implements(SlashCommand, PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    osu_api_test_link = (
        "https://osu.ppy.sh/api/"
        f"get_beatmaps?k={settings.OSU_API_KEY}"
        f"&b=1"
    )

    time_start = time.time()
    r = await glob.osu.get(osu_api_test_link)
    time_end = time.time()

    diff = int((time_end - time_start) * 1000)

    osu_text = f"osu!api: **{diff}ms** `{r.status}`\n"

    secret_api_test_link = settings.SUPER_SECRET_API_LINK.format(100)
    time_start = time.time()
    r = await glob.osu.get(secret_api_test_link)
    time_end = time.time()

    diff = int((time_end - time_start) * 1000)

    secret_api_text = f"secret api: **{diff}**ms `{r.status}`\n"

    await ctx.respond("Pong!\n" + osu_text + secret_api_text)

def load(bot: lightbulb.BotApp):
    print("Loaded debug plugin")
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
