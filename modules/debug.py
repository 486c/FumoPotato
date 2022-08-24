from __future__ import annotations
from typing import Optional

import traceback
import pprint
import math
import time
import datetime
import sys

import lightbulb
from lightbulb import PrefixCommand, SlashCommand

import glob
import settings

plugin = lightbulb.Plugin("debug")

blacklist = ['__import__', 'open', 'subprocess', 'capture_output', 'ssh', 'stdout', 'socat', 'exec']

def get_code_from_msg(
    prefix: str,
    cmd: str,
    text: str
) -> Optional[str]:
    code_raw = text.replace(f"{prefix}{cmd} ", "")

    if code_raw.startswith("```"):
        # multiline code block

        # Check if code block is correct
        if not code_raw.endswith("```"):
            return None

        code_raw = code_raw.removeprefix("```")
        code_raw = code_raw.removesuffix("```")
        
        # Remove syntax highlighters
        for lang_code in ("py", "python"):
            if code_raw.startswith(lang_code):
                code_raw.replace(lang_code, "")

    elif code_raw.startswith("`"):
        # code block

        # Check if code block is correct
        if not code_raw.endswith("`"):
            return None

        code_raw = code_raw.removeprefix("`")
        code_raw = code_raw.removesuffix("`")
    else:
        # just text
        pass

    code_raw = "\n".join(l for l in code_raw.split("\n") if l)
    code_raw = code_raw.strip("`\n\t ")

    return code_raw

@plugin.command()
@lightbulb.command("py", "Execute python code")
@lightbulb.implements(PrefixCommand)
async def py(ctx: lightbulb.Context) -> None:
    if ctx.guild_id not in (760864525980401684, 662973494459629568):
        await ctx.respond("Not allowed!")
        return

    code = get_code_from_msg(
        ctx.prefix,
        ctx.invoked_with,
        ctx.event.content
    )

    if code is None:
        await ctx.respond(
            "Failed to parse code from message!",
            reply=True)
        return

    if len(code) < 5:
        await ctx.respond(
            "No code is provided!",
            reply=True)
        return

    # Looking for blacklisted words >.<
    for word in blacklist:
        if code.find(word) > 0:
            await ctx.respond(
                "Nice try!",
                reply=True
            )
            return

    namespace = {
        "math": math,
        "time": time,
        "datetime": datetime,
    }

    code_text = f" {code}".replace("\n", "\n ")
    func_def = f"async def __py(ctx):\n{code_text}"

    try:
        exec(func_def, namespace)
        ret = await namespace["__py"](ctx)
    except:
        await ctx.respond(
            f"```\n{traceback.format_exc()}```",
            reply=True
        )
        return
    del namespace
    if not isinstance(ret, str):
        oversize = sys.getsizeof(ret) - (3 * 1024)
        if oversize > 0:
            await ctx.respond(
                f"Response is way too large!! Got {oversize}B",
                reply=True
            )
            return

        ret = pprint.pformat(ret, compact=True)

    if len(ret) > 2000:
        ret = ret[:1999]

    if ret is not None and ret != "None":
        await ctx.respond(f"```{ret}```", reply=True)

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

    secret_api_text = f"fallback api: **{diff}ms** `{r.status}`\n"

    await ctx.respond("Pong!\n" + osu_text + secret_api_text)

def load(bot: lightbulb.BotApp):
    print("Loaded debug plugin")
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
