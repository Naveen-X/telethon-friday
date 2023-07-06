"""DA.GD helpers in @UniBorg
Available Commands:
.isup URL
.dns google.com
.url <long url>
.unshort <short url>"""
import requests

from fridaybot.utils import friday_on_cmd


@friday.on(friday_on_cmd("dns (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/dns/{input_str}"
    if response_api := requests.get(sample_url).text:
        await event.edit(f"DNS records of {input_str} are \n{response_api}")
    else:
        await event.edit(f"i can't seem to find {input_str} on the internet")


@friday.on(friday_on_cmd("url (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    sample_url = f"https://da.gd/s?url={input_str}"
    if response_api := requests.get(sample_url).text:
        await event.edit(f"Generated {response_api} for {input_str}.")
    else:
        await event.edit("something is wrong. please try again later.")


@friday.on(friday_on_cmd("unshort (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if not input_str.startswith("http"):
        input_str = f"http://{input_str}"
    r = requests.get(input_str, allow_redirects=False)
    if str(r.status_code).startswith("3"):
        await event.edit(
            f'Input URL: {input_str}\nReDirected URL: {r.headers["Location"]}'
        )
    else:
        await event.edit(f"Input URL {input_str} returned status_code {r.status_code}")
