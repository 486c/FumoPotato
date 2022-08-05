from __future__ import annotations

from typing import Optional

import lightbulb
from lightbulb import PrefixCommand, SlashCommand

import glob
import settings

plugin = lightbulb.Plugin("debug")

@plugin.command()
@lightbulb.command("ping", "See if bot alive")
@lightbulb.implements(SlashCommand, PrefixCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await ctx.respond("Pong!")

def load(bot: lightbulb.BotApp):
    print("Loaded debug plugin")
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
