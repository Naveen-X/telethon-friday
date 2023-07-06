"""Default Permission in Telegram 5.0.1
Available Commands: .lock <option>, .unlock <option>, .locks
API Options: msg, media, sticker, gif, gamee, ainline, gpoll, adduser, cpin, changeinfo
DB Options: bots, commands, email, forward, url"""

from telethon import events, functions, types

from fridaybot.modules.sql_helper.locks_sql import get_locks, is_locked, update_lock
from fridaybot.utils import edit_or_reply, friday_on_cmd, sudo_cmd


@friday.on(friday_on_cmd("lock( (?P<target>\S+)|$)"))
@friday.on(sudo_cmd("lock( (?P<target>\S+)|$)", allow_sudo=True))
async def _(event):
    mrhackerguy = await edit_or_reply(event, "Processing")
    # Space weirdness in regex required because argument is optional and other
    # commands start with ".lock"
    if event.fwd_from:
        return
    input_str = event.pattern_match.group("target")
    peer_id = event.chat_id
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, True)
        await mrhackerguy.edit(f"Locked {input_str}")
    else:
        msg = None
        media = None
        sticker = None
        gif = None
        gamee = None
        ainline = None
        gpoll = None
        adduser = None
        cpin = None
        changeinfo = None
        if input_str:
            if "msg" in input_str:
                msg = True
            if "media" in input_str:
                media = True
            if "sticker" in input_str:
                sticker = True
            if "gif" in input_str:
                gif = True
            if "gamee" in input_str:
                gamee = True
            if "ainline" in input_str:
                ainline = True
            if "gpoll" in input_str:
                gpoll = True
            if "adduser" in input_str:
                adduser = True
            if "cpin" in input_str:
                cpin = True
            if "changeinfo" in input_str:
                changeinfo = True
        banned_rights = types.ChatBannedRights(
            until_date=None,
            # view_messages=None,
            send_messages=msg,
            send_media=media,
            send_stickers=sticker,
            send_gifs=gif,
            send_games=gamee,
            send_inline=ainline,
            send_polls=gpoll,
            invite_users=adduser,
            pin_messages=cpin,
            change_info=changeinfo,
        )
        try:
            result = await borg(  # pylint:disable=E0602
                functions.messages.EditChatDefaultBannedRightsRequest(
                    peer=peer_id, banned_rights=banned_rights
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mrhackerguy.edit(str(e))
        else:
            await mrhackerguy.edit(
                "Current Chat Default Permissions Changed Successfully, in API"
            )


@friday.on(friday_on_cmd("unlock ?(.*)"))
@friday.on(sudo_cmd("unlock ?(.*)", allow_sudo=True))
async def _(event):
    starkgang = await edit_or_reply(event, "Processing")
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    if input_str in (("bots", "commands", "email", "forward", "url")):
        update_lock(peer_id, input_str, False)
        await starkgang.edit(f"UnLocked {input_str}")
    else:
        await starkgang.edit("Use `.lock` without any parameters to unlock API locks")


@friday.on(friday_on_cmd("curenabledlocks"))
@friday.on(friday_on_cmd("curenabledlocks", allow_sudo=True))
async def _(event):
    pikachu = await edit_or_reply(event, "Processing")
    if event.fwd_from:
        return
    res = ""
    if current_db_locks := get_locks(event.chat_id):
        res = (
            "Following are the DataBase locks in this chat: \n"
            + f"👉 `bots`: `{current_db_locks.bots}`\n"
        )
        res += f"👉 `commands`: `{current_db_locks.commands}`\n"
        res += f"👉 `email`: `{current_db_locks.email}`\n"
        res += f"👉 `forward`: `{current_db_locks.forward}`\n"
        res += f"👉 `url`: `{current_db_locks.url}`\n"
    else:
        res = "There are no DataBase locks in this chat"
    current_chat = await event.get_chat()
    try:
        current_api_locks = current_chat.default_banned_rights
    except AttributeError as e:
        logger.info(str(e))
    else:
        res += "\nFollowing are the API locks in this chat: \n"
        res += f"👉 `msg`: `{current_api_locks.send_messages}`\n"
        res += f"👉 `media`: `{current_api_locks.send_media}`\n"
        res += f"👉 `sticker`: `{current_api_locks.send_stickers}`\n"
        res += f"👉 `gif`: `{current_api_locks.send_gifs}`\n"
        res += f"👉 `gamee`: `{current_api_locks.send_games}`\n"
        res += f"👉 `ainline`: `{current_api_locks.send_inline}`\n"
        res += f"👉 `gpoll`: `{current_api_locks.send_polls}`\n"
        res += f"👉 `adduser`: `{current_api_locks.invite_users}`\n"
        res += f"👉 `cpin`: `{current_api_locks.pin_messages}`\n"
        res += f"👉 `changeinfo`: `{current_api_locks.change_info}`\n"
    await pikachu.edit(res)


@friday.on(events.MessageEdited())  # pylint:disable=E0602
@friday.on(events.NewMessage())  # pylint:disable=E0602
async def check_incoming_messages(event):
    # TODO: exempt admins from locks
    peer_id = event.chat_id
    if is_locked(peer_id, "commands"):
        is_command = False
        if entities := event.message.entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityBotCommand):
                    is_command = True
        if is_command:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(f"I don't seem to have ADMIN permission here. \n`{str(e)}`")
                update_lock(peer_id, "commands", False)
    if is_locked(peer_id, "forward"):
        if event.fwd_from:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(f"I don't seem to have ADMIN permission here. \n`{str(e)}`")
                update_lock(peer_id, "forward", False)
    if is_locked(peer_id, "email"):
        is_email = False
        if entities := event.message.entities:
            for entity in entities:
                if isinstance(entity, types.MessageEntityEmail):
                    is_email = True
        if is_email:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(f"I don't seem to have ADMIN permission here. \n`{str(e)}`")
                update_lock(peer_id, "email", False)
    if is_locked(peer_id, "url"):
        is_url = False
        if entities := event.message.entities:
            for entity in entities:
                if isinstance(
                    entity, (types.MessageEntityTextUrl, types.MessageEntityUrl)
                ):
                    is_url = True
        if is_url:
            try:
                await event.delete()
            except Exception as e:
                await event.reply(f"I don't seem to have ADMIN permission here. \n`{str(e)}`")
                update_lock(peer_id, "url", False)


@friday.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    # TODO: exempt admins from locks
    # check for "lock" "bots"
    if not is_locked(event.chat_id, "bots"):
        return
        # bots are limited Telegram accounts,
        # and cannot join by themselves
    if event.user_added:
        users_added_by = event.action_message.sender_id
        is_ban_able = False
        rights = types.ChatBannedRights(until_date=None, view_messages=True)
        added_users = event.action_message.action.users
        for user_id in added_users:
            user_obj = await borg.get_entity(user_id)
            if user_obj.bot:
                is_ban_able = True
                try:
                    await borg(
                        functions.channels.EditBannedRequest(
                            event.chat_id, user_obj, rights
                        )
                    )
                except Exception as e:
                    await event.reply(f"I don't seem to have ADMIN permission here. \n`{str(e)}`")
                    update_lock(event.chat_id, "bots", False)
                    break
        if Config.G_BAN_LOGGER_GROUP is not None and is_ban_able:
            ban_reason_msg = await event.reply(
                f"!warn [user](tg://user?id={users_added_by}) Please Do Not Add BOTs to this chat."
            )
