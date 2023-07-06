"""Get ID of any Telegram media, or any user
Syntax: .get_id"""
from telethon.utils import pack_bot_file_id

from fridaybot import CMD_HELP
from fridaybot.utils import edit_or_reply, friday_on_cmd, sudo_cmd


@friday.on(friday_on_cmd("get_id"))
@friday.on(sudo_cmd("get_id", allow_sudo=True))
async def _(event):
    starkisgreat = await edit_or_reply(event, "Processing")
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await starkisgreat.edit(
                f"Current Chat ID: `{str(event.chat_id)}`\nFrom User ID: `{str(r_msg.sender_id)}`\nBot API File ID: `{bot_api_file_id}`"
            )
        else:
            await starkisgreat.edit(
                f"Current Chat ID: `{str(event.chat_id)}`\nFrom User ID: `{str(r_msg.sender_id)}`"
            )
    else:
        await starkisgreat.edit(f"Current Chat ID: `{str(event.chat_id)}`")


CMD_HELP.update(
    {
        "get_id": "**Get Id**\
\n\n**Syntax : **`.get_id <reply to media or any message>`\
\n**Usage :** Get ID of any Telegram media, or any user."
    }
)
