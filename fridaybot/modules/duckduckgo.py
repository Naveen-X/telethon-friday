"""use command .ducduckgo"""

from uniborg.util import friday_on_cmd

from fridaybot import CMD_HELP


@friday.on(friday_on_cmd("ducduckgo (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if (
        sample_url := f'https://duckduckgo.com/?q={input_str.replace(" ", "+")}'
    ):
        link = sample_url.rstrip()
        await event.edit(f"Let me 🦆 DuckDuckGo that for you:\n🔎 [{input_str}]({link})")
    else:
        await event.edit("something is wrong. please try again later.")


CMD_HELP.update(
    {
        "duckduckgo": "**Duckduckgo**\
\n\n**Syntax : **`.ducduckgo <query>`\
\n**Usage :** get duckduckgo search query link"
    }
)
