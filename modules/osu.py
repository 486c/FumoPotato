from __future__ import annotations

import lightbulb

from lightbulb import PrefixCommand, SlashCommand

import glob

plugin = lightbulb.Plugin("osu")

@plugin.command()
@lightbulb.command("ping", "test")
@lightbulb.implements(PrefixCommand, SlashCommand)
async def test(ctx: lightbulb.Context) -> None:
    await glob.osu.get()
    await ctx.respond("pong!")

def load(bot: lightbulb.BotApp):
    print("Loaded osu! plugin")
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
