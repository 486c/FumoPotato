from __future__ import annotations

import os

import hikari
import lightbulb
import miru

from lightbulb import commands, context
from lightbulb.ext import tasks

import settings
import glob
import osu_api

bot = lightbulb.BotApp(
	token = settings.DISCORD_TOKEN,
	prefix = lightbulb.when_mentioned_or(';;'),
	intents = hikari.Intents.ALL,
	delete_unbound_commands = True,
	case_insensitive_prefix_commands = True,
	owner_ids = (278836450475376641),
	allow_color=True
)
tasks.load(bot)
miru.load(bot)

@bot.listen(hikari.StartingEvent)
async def on_start(event: hikari.StartingEvent) -> None:
    bot.load_extensions_from("./modules/", must_exist=True)
    glob.osu = osu_api.osuAPI()

@bot.listen(hikari.StartedEvent)
async def on_ready(event: hikari.StartedEvent) -> None:
    await bot.update_presence(
        status= hikari.Status.ONLINE
    )
    bot.unsubscribe(hikari.StartingEvent, on_start)
    bot.unsubscribe(hikari.StartedEvent, on_ready)

@bot.listen(hikari.StoppingEvent)
async def on_stop(event: hikari.StoppedEvent) -> None:
    await glob.osu.close()

if __name__ == "__main__":
    if os.name != "nt":
        import uvloop
        uvloop.install()

    bot.run()
