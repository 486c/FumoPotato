from __future__ import annotations

from typing import Optional

import lightbulb
from lightbulb import PrefixCommand, SlashCommand

import glob
import settings

from helpers import CountryLeaderboard

plugin = lightbulb.Plugin("osu")

def get_bid_from_url(url: str) -> Optional[int]:
    count = url.count('/')
    splitted = url.split('/')
    
    if count == 5:
        return int(splitted[5])
    if count == 4:
        return int(splitted[4])

    return None

def get_bid_from_message(msg: hikari.Message) -> Optional[int]:
    url = ""
    
    # hardcoded but i dont care
    # owo#0498
    if msg.author.id == 289066747443675143:
        if len(msg.embeds) == 1:
            url = msg.embeds[0].author.url

    # Bathbot#0459
    if msg.author.id == 297073686916366336:
        if len(msg.embeds) == 1:
            url = msg.embeds[0].url
    
    # mikazuki#9812
    if msg.author.id == 839937716921565252:
        if len(msg.embeds) == 1:
            url = msg.embeds[0].url
    # Pekofor#8835
    if msg.author.id == 925723087234826300:
        if len(msg.embeds) == 1:
            url = msg.embeds[0].url

    return get_bid_from_url(url)

@plugin.command()
@lightbulb.option("link", "beatmap link", str, required=False)
@lightbulb.command("lb", "Show country leaderboard")
@lightbulb.implements(PrefixCommand)
async def leaderboard_prefix(ctx: lightbulb.Context) -> None:
    bid: int = None

    msg = ctx.event.message

    # Getting beatmap_id
    if ctx.options.link is None:
        msg_ref = msg.referenced_message
        
        # Trying to fetch beatmap_id from reply
        if msg_ref is not None:
            bid = get_bid_from_message(msg_ref)
        
        # Searching for valid score message
        if msg_ref is None:
            channel = ctx.event.get_channel()
            async for msg in channel.fetch_history():
                bid = get_bid_from_message(msg)
                if bid is not None:
                    break

    # Getting beatmap_id directly from link
    if ctx.options.link is not None:
        bid = get_bid_from_url(ctx.options.link)
    
    # Checking if beatmap_id was found
    if bid is None:
        await ctx.respond(
            "Can't find any valid scores!",
            reply=True
        )
        return

    # Getting beatmap from osu!api
    b = await glob.osu.get_beatmaps(bid)
    #TODO checks

    # Getting country scores
    #TODO checks
    r = await glob.osu.get(settings.SUPER_SECRET_API_LINK.format(bid))
    scores_json = await r.json()

    view = CountryLeaderboard(scores_json['scores'], b)
    emb = view.build_embed(1) 
    listen = await msg.respond(embed=emb, components=view.build())
    view.start(listen)
    await view.wait()

    # Remove all components after timeout
    await listen.edit(components=None)

def load(bot: lightbulb.BotApp):
    print("Loaded osu! plugin")
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
