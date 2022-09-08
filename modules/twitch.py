from __future__ import annotations

from typing import Optional

import lightbulb
from lightbulb import SlashCommand
from lightbulb.checks import has_guild_permissions

import hikari
from hikari import Permissions

import glob

from apscheduler.triggers.cron import CronTrigger

plugin = lightbulb.Plugin("twitch")

@plugin.command()
@lightbulb.app_command_permissions(Permissions.MANAGE_NICKNAMES, dm_enabled=False)
@lightbulb.option("name", "twitch username", str, required=True)
@lightbulb.command("twitch_add", "Add new twitch channel to announcer")
@lightbulb.implements(SlashCommand)
async def twitch_add(ctx: lightbulb.Context) -> None:
    s = await glob.mongo['twitch'].find_one({'name': ctx.options.name})
    twitch_name = ctx.options.name

    if s is None:
        data = {
            'name': twitch_name,
            'online': False,
            'channels': [],
        }

        await glob.mongo['twitch'].insert_one(data)
        s = await glob.mongo['twitch'].find_one({'name': twitch_name})

    if ctx.channel_id in s['channels']:
        await ctx.respond(
            f"`{twitch_name}` already added to current channel!"
        )
        return

    await glob.mongo['twitch'].update_one(
        {'_id': s['_id']},
        {'$push': { 'channels': ctx.channel_id}}
    )

    await ctx.respond(
        f"`{twitch_name}` seccessfuly added to current channel!"
    )

@plugin.command()
@lightbulb.app_command_permissions(dm_enabled=False)
@lightbulb.command("twitch_list", "List all streamers on current channel")
@lightbulb.implements(SlashCommand)
async def twitch_list(ctx: lightbulb.Context) -> None:
    c = glob.mongo['twitch']
    response = "\n"
    async for d in c.find({'channels': {'$in': [ctx.channel_id]}}):
        response += f"{d['name']}\n"

    if len(response) == 0:
        await ctx.respond("Can't find streamers on current channel")
    else:
        await ctx.respond(f"```{response}```")

@plugin.command()
@lightbulb.app_command_permissions(Permissions.MANAGE_NICKNAMES, dm_enabled=False)
@lightbulb.option("name", "twitch username", str, required=True)
@lightbulb.command("twitch_remove", "Remove twitch channel from announcer")
@lightbulb.implements(SlashCommand)
async def twitch_remove(ctx: lightbulb.Context) -> None:
    twitch_name = ctx.options.name
    s = await glob.mongo['twitch'].find_one(
        {'channels': {'$in': [ctx.channel_id]}},
        {'name': twitch_name},
    )

    if s is None:
        await ctx.respond(f"`{twitch_name}` is not found in current channel")
        return

    await glob.mongo['twitch'].update_one(
        {'_id': s['_id']},
        {'$pull': { 'channels': ctx.channel_id}}
    )

    await ctx.respond(f"`{twitch_name}` has been removed from current channel")

    pass

async def global_check() -> None:
    c = glob.mongo['twitch']
    async for d in c.find():
        json = await glob.twitch.get_stream(d['name'])

        if json is None:
            if d['online'] == True:
                c.update_one(
                    {'_id': d['_id']},
                    {'$set': {'online': False}}
                )

            continue

        if d['online'] == False and json['type'] == 'live':
            c.update_one(
                {'_id': d['_id']},
                {'$set': {'online': True}}
            )
            emb = hikari.Embed()
            emb.title = f"{d['name']} is online!"
            emb.description = f"**{json['title']}**"
            emb.url = f"https://twitch.tv/{d['name']}"
            emb.color = hikari.Color(0x97158a)
            emb.set_image(f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{d['name']}-1280x720.jpg")

            emb.set_footer(
                json['title'],
                icon=f"https://static-cdn.jtvnw.net/ttv-boxart/{json['game_id']}-250x250.jpg"
            )

            for channel_id in d['channels']:
                await plugin.bot.rest.create_message(channel_id, embed=emb)

@plugin.listener(hikari.StartedEvent)
async def on_started(_: hikari.StartedEvent) -> None:
    plugin.app.d.sched.add_job(global_check, 'interval', minutes=1)

def load(bot: lightbulb.BotApp):
    print("Loaded twitch plugin")
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
