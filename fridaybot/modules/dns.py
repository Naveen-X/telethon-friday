"""DA.GD helpers in @UniBorg
Available Commands:
.isup URL
.dns google.com
.url <long url>
.unshort <short url>"""
import requests

from fridaybot import CMD_HELP
from fridaybot.utils import edit_or_reply, friday_on_cmd, sudo_cmd


@friday.on(friday_on_cmd("dns (.*)"))
@friday.on(sudo_cmd("dns (.*)", allow_sudo=True))
async def _(event):
    starky = await edit_or_reply(event, "Processing.....")
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/dns/{input_str}"
    if response_api := requests.get(sample_url).text:
        await starky.edit(f"DNS records of {input_str} are \n{response_api}")
    else:
        await starky.edit(f"i can't seem to find {input_str} on the internet")


@friday.on(friday_on_cmd("url (.*)"))
@friday.on(sudo_cmd("dns (.*)", allow_sudo=True))
async def _(event):
    starkxd = await edit_or_reply(event, "Processing....")
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url={input_str}"
    if response_api := requests.get(sample_url).text:
        await starkxd.edit(f"Generated {response_api} for {input_str}.")
    else:
        await starkxd.edit("something is wrong. please try again later.")


@friday.on(friday_on_cmd("unshort (.*)"))
async def _(event):
    sadness = await edit_or_reply(event, "Processing...")
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = f"http://{input_str}"
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await sadness.edit(
            f'Input URL: {input_str}\nReDirected URL: {r.headers["Location"]}'
        )
    else:
        await sadness.edit(
            f"Input URL {input_str} returned status_code {r.status_code}"
        )


CMD_HELP.update(
    {
        "dns": "**Dns**\
\n\n**Syntax : **`.dns <site link>`\
\n**Usage :** it provides DNS records of given site.\
\n\n**Syntax : **`.url <site link>`\
\n**Usage :** it shortens given URL.\
\n\n**Syntax : **`.unshort <shorten link>`\
\n**Usage :** it unshortens the given short link."
    }
)
