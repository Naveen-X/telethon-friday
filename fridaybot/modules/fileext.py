"""Get info about a File Extension
Syntax: .filext EXTENSION"""
import requests
from bs4 import BeautifulSoup
from uniborg.util import friday_on_cmd

from fridaybot import CMD_HELP


@friday.on(friday_on_cmd(pattern="filext (.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    sample_url = "https://www.fileext.com/file-extension/{}.html"
    input_str = event.pattern_match.group(1).lower()
    response_api = requests.get(sample_url.format(input_str))
    status_code = response_api.status_code
    if status_code == 200:
        raw_html = response_api.content
        soup = BeautifulSoup(raw_html, "html.parser")
        ext_details = soup.find_all("td", {"colspan": "3"})[-1].text
        await event.edit(
            f"**File Extension**: `{input_str}`\n**Description**: `{ext_details}`"
        )
    else:
        await event.edit(
            f"https://www.fileext.com/ responded with {status_code} for query: {input_str}"
        )


CMD_HELP.update(
    {
        "fileext": "**File Extension**\
\n\n**Syntax : **`.filext <extension>`\
\n**Usage :** Gives details about the extension."
    }
)
