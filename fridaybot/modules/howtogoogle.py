# Modded from dagd.py
"""
Animate How To Google
Command .ggl Search Query
By @loxxi
"""

import requests

from fridaybot import CMD_HELP
from fridaybot.utils import friday_on_cmd


@friday.on(friday_on_cmd("ggl (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = f'https://da.gd/s?url=https://lmgtfy.com/?q={input_str.replace(" ", "+")}%26iie=1'
    if response_api := requests.get(sample_url).text:
        await event.edit(
            f"[{input_str}]({response_api.rstrip()})\n`Thank me Later 🙃` "
        )
    else:
        await event.edit("something is wrong. please try again later.")


CMD_HELP.update(
    {
        "howtogoogle": "**How To Google**\
\n\n**Syntax : **`.ggl <search query>`\
\n**Usage :** Animates how to Google with search query."
    }
)
