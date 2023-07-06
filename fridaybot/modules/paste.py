"""IX.IO pastebin like site
Syntax: .paste
From Pornhub"""
import logging
import os
from datetime import datetime

import requests
from uniborg.util import friday_on_cmd, sudo_cmd

from fridaybot import CMD_HELP

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.WARNING
)


def progress(current, total):
    logger.info(
        f"Downloaded {current} of {total}\nCompleted {current / total * 100}"
    )


@friday.on(friday_on_cmd("paste ?(.*)"))
@friday.on(sudo_cmd("paste ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    datetime.now()
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if input_str := event.pattern_match.group(1):
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
            message = "".join(m.decode("UTF-8") for m in m_list)
            os.remove(downloaded_file_name)
        else:
            message = previous_message.message
    else:
        await event.edit("Give Some Text Or File To Paste")
    name = "ok"
    if previous_message.media:
        name = await borg.download_media(
            previous_message, Config.TMP_DOWNLOAD_DIRECTORY, progress_callback=progress
        )
    downloaded_file_name = name
    if downloaded_file_name.endswith(".py"):
        py_file = "" + ".py"
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}{py_file}"
        raw = f"https://nekobin.com/raw/{key}{py_file}"
    else:
        data = message
        key = (
            requests.post("https://nekobin.com/api/documents", json={"content": data})
            .json()
            .get("result")
            .get("key")
        )
        url = f"https://nekobin.com/{key}"
        raw = f"https://nekobin.com/raw/{key}"

    reply_text = f"Pasted Text [neko]({url})\n Raw ? [View Raw]({raw})"
    await event.edit(reply_text)


CMD_HELP.update(
    {
        "paste": "**Paste**\
\n\n**Syntax : **`.paste <reply to your text file>`\
\n**Usage :** this plugin automatically uploades and pastes replied text file to nekobin.com "
    }
)
