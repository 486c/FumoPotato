from __future__ import annotations

import miru
import hikari
from hikari import ButtonStyle

from typing import Sequence

from utils import get_emoji_from_rank

from datetime import datetime

class CountryLeaderboard(miru.View):
    def __init__(self, scores, b) -> None:
        super().__init__(timeout=10)

        self.scores: Sequence[dict] = scores
        self.beatmap: dict = b

        self.cur_page: int = 1
        self.total_pages: int = 1

        pages_value: float = float(len(scores))/10.0
        if pages_value > 1:
            self.total_pages = int(pages_value)
    
    def build_embed(self, page: int) -> hikari.Embed:
        emb = hikari.Embed()

        author_text = (
            f"Total scores: {len(self.scores)} "
            f"[{self.cur_page}/{self.total_pages}]"
        )

        emb.set_author(name=author_text)
        emb.color = hikari.Color(0x0d3636)
        emb.set_thumbnail(
            "https://assets.ppy.sh/beatmaps/"
            f"{self.beatmap['beatmapset_id']}"
            "/covers/list.jpg"
        )
        emb.set_footer(
            f"{self.beatmap['artist']} - {self.beatmap['title']} "
            f"[{self.beatmap['version']}]"
        )
        
        desc = ""
        s_max = 10
        s_min = 0
        
        if(page > 1):
            s_min = (page-1)*10
            s_max = (page)*10

        for index, score in enumerate(self.scores[s_min:s_max]):
            mods = "+"

            if len(score['mods']) == 0:
                mods += "NM"
            for m in score['mods']:
                mods += m

            score_formatted = "{:,}".format(int(score['score']))
            acc = "{:.2f}".format(float(score['accuracy']) * 100)
            x300 = score['statistics']['count_300']
            x100 = score['statistics']['count_100']
            x50 = score['statistics']['count_50']
            xmiss = score['statistics']['count_miss']
            dt = datetime.strptime(
                score['created_at'],
                '%Y-%m-%dT%H:%M:%S%z'
            )
            timestamp_text = f"<t:{int(dt.timestamp())}:R>"

            pp = ""
            if(score['pp'] == None):
                pp = "NaN"
            else:
                pp = "{:.2f}".format(float(score['pp']))

            rank = get_emoji_from_rank(score['rank'])
            profile_text = (
                    "["
                    f"{score['user']['username']}"
                    "]"
                    "("
                    "https://osu.ppy.sh/u/"
                    f"{score['user']['id']}"
                    ")"
            )

            desc += (
                f"**{(index+(page-1)*10)+1}**. "
                f"{profile_text} "
                f"**{mods}**"
                "\n"
                f"{rank} • "
                f"{acc}% • "
                f"{pp}pp"
                "\n"
                f"{score_formatted} • "
                f"x{score['max_combo']} • "
                f"[{x300}/{x100}/{x50}/{xmiss}]"
                "\n"
                f"{timestamp_text}"
                "\n"
            )

        emb.description = desc

        return emb

    @miru.button(label="Previous page", style=ButtonStyle.PRIMARY)
    async def left_button(
        self,
        button: miru.Button,
        ctx: miru.Context
    ) -> None:
        if self.cur_page - 1 < 1:
            return

        self.cur_page -= 1
        emb = self.build_embed(self.cur_page)

        await ctx.edit_response(embed=emb)

    @miru.button(label="Next page", style=ButtonStyle.PRIMARY)
    async def right_button(
        self,
        button: miru.Button,
        ctx: miru.Context
    ) -> None:
        if self.cur_page + 1 > self.total_pages:
            return

        self.cur_page += 1
        emb = self.build_embed(self.cur_page)

        await ctx.edit_response(embed=emb)
