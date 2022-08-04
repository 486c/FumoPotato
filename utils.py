from __future__ import annotations

def get_emoji_from_rank(rank: str) -> str:
    r = ""

    if rank == "D":
        r = "<:r_D:1004444323703701545>"
    if rank == "C":
        r = "<:r_C:1004444033524957235>"
    if rank == "B":
        r = "<:r_B:1004444032149233696>"
    if rank == "A":
        r = "<:r_A:1004444322365702204>"
    if rank == "S":
        r = "<:r_S:1004444324840349759>"
    if rank == "SH":
        r = "<:r_SH:1004444326669066270>"
    if rank == "X":
        r = "<:r_X:1004444328082538546>"
    if rank == "XH":
        r = "<:r_XH:1004444329365999766>"

    return r
