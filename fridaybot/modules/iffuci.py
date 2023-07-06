"""iffuci.tk pastebin site
Code written by @loxxi {iffuci}
Syntax: .iffuci"""
import os
from datetime import datetime

import requests

from fridaybot.utils import edit_or_reply, friday_on_cmd, sudo_cmd


def progress(current, total):
    logger.info(
        f"Downloaded {current} of {total}\nCompleted {current / total * 100}"
    )


@friday.on(friday_on_cmd(pattern="iffuci ?(.*)"))
@friday.on(sudo_cmd(pattern="iffuci ?(.*)", allow_sudo=True))
async def _(event):
    crackexy = await edit_or_reply(event, "Processing")
    if event.fwd_from:
        return
    start = datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    input_str = event.pattern_match.group(1)
    message = "SYNTAX: `.iffuci <long text to include>`"
    if input_str:
        message = input_str
    elif event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        if previous_message.media:
            downloaded_file_name = await borg.download_media(
                previous_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=progress,
            )
            m_list = None
            with open(downloaded_file_name, "rb") as fd:
                m_list = fd.readlines()
            message = "".join(m.decode("UTF-8") + "\r\n" for m in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        message = "SYNTAX: `.iffuci <long text to include>`"
    url = "https://www.iffuci.tk/documents"
    r = requests.post(url, data=message.encode("UTF-8")).json()
    url = f"https://iffuci.tk/{r['key']}"
    end = datetime.now()
    ms = (end - start).seconds
    if r["isUrl"]:
        nurl = f"https://iffuci.tk/v/{r['key']}"
        await crackexy.edit(
            f"code is pasted to {url} in {ms} seconds. GoTo Original URL: {nurl}"
        )
    else:
        await crackexy.edit(f"code is pasted to {url} in {ms} seconds")
