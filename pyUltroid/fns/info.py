# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.


# -----------------Random Stuff--------------

import math

from telethon.tl import functions, types

from .. import LOGS

# -----------
# @buddhhu


async def get_uinfo(e):
    user, data = None, None
    reply = await e.get_reply_message()
    if reply:
        user = await e.client.get_entity(reply.sender_id)
        data = e.pattern_match.group(1)
    else:
        ok = e.pattern_match.group(1).split(maxsplit=1)
        if len(ok) > 1:
            data = ok[1]
        try:
            user = await e.client.get_entity(await e.client.parse_id(ok[0]))
        except IndexError:
            pass
        except ValueError as er:
            await e.eor(str(er))
            return None, None
    return user, data


# Random stuffs dk who added


async def get_chat_info(chat, event):
    if isinstance(chat, types.Channel):
        chat_info = await event.client(functions.channels.GetFullChannelRequest(chat))
    elif isinstance(chat, types.Chat):
        chat_info = await event.client(functions.messages.GetFullChatRequest(chat))
    else:
        return await event.eor("```Use this for Group/Channel.```")
    full = chat_info.full_chat
    chat_photo = full.chat_photo
    broadcast = getattr(chat, "broadcast", False)
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat.title
    try:
        msg_info = await event.client(
            functions.messages.GetHistoryRequest(
                peer=chat.id,
                offset_id=0,
                offset_date=None,
                add_offset=-0,
                limit=0,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )
    except Exception as er:
        msg_info = None
        if not event.client._bot:
            LOGS.exception(er)
    first_msg_valid = bool(
        msg_info and msg_info.messages and msg_info.messages[0].id == 1
    )

    creator_valid = bool(first_msg_valid and msg_info.users)
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = (
        msg_info.users[0].first_name
        if creator_valid and msg_info.users[0].first_name is not None
        else "Deleted Account"
    )
    creator_username = (
        msg_info.users[0].username
        if creator_valid and msg_info.users[0].username is not None
        else None
    )
    created = msg_info.messages[0].date if first_msg_valid else None
    if not isinstance(chat.photo, types.ChatPhotoEmpty):
        dc_id = chat.photo.dc_id
    else:
        dc_id = "Null"

    restricted_users = getattr(full, "banned_count", None)
    members = getattr(full, "participants_count", chat.participants_count)
    admins = getattr(full, "admins_count", None)
    banned_users = getattr(full, "kicked_count", None)
    members_online = getattr(full, "online_count", 0)
    group_stickers = (
        full.stickerset.title if getattr(full, "stickerset", None) else None
    )
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = getattr(full, "read_inbox_max_id", None)
    messages_sent_alt = getattr(full, "read_outbox_max_id", None)
    exp_count = getattr(full, "pts", None)
    supergroup = "<b>Yes</b>" if getattr(chat, "megagroup", None) else "No"
    creator_username = "@{}".format(creator_username) if creator_username else None

    if admins is None:
        try:
            participants_admins = await event.client(
                functions.channels.GetParticipantsRequest(
                    channel=chat.id,
                    filter=types.ChannelParticipantsAdmins(),
                    offset=0,
                    limit=0,
                    hash=0,
                )
            )
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            LOGS.info(f"``Exception: {e}``")
    caption = "<blockquote>ℹ️ <b>[<u>CHAT INFO</u>]</b>\n</blockquote>"
    caption += f"<blockquote>🆔 <b>ID:</b> <code>{chat.id}</code>\n</blockquote>"
    if chat_title is not None:
        caption += f"<blockquote>📛 <b>{chat_type} name:</b> <code>{chat_title}</code>\n</blockquote>"
    if chat.username:
        caption += f"<blockquote>🔗 <b>Link:</b> @{chat.username}\n</blockquote>"
    else:
        caption += f"<blockquote>🗳 <b>{chat_type} type:</b> Private\n</blockquote>"
    if creator_username:
        caption += f"<blockquote>🖌 <b>Creator:</b> {creator_username}\n</blockquote>"
    elif creator_valid:
        caption += f'<blockquote>🖌 <b>Creator:</b> <a href="tg://user?id={creator_id}">{creator_firstname}</a>\n</blockquote>'
    if created:
        caption += f"<blockquote>🖌 <b>Created:</b> <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n</blockquote>"
    else:
        caption += f"<blockquote>🖌 <b>Created:</b> <code>{chat.date.date().strftime('%b %d, %Y')} - {chat.date.time()}</code> ⚠\n</blockquote>"
    caption += f"<blockquote>🗡 <b>Data Centre ID:</b> {dc_id}\n</blockquote>"
    if exp_count is not None:
        chat_level = int((1 + math.sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"<blockquote>⭐️ <b>{chat_type} level:</b> <code>{chat_level}</code>\n</blockquote>"
    if messages_viewable is not None:
        caption += f"<blockquote>💬 <b>Viewable messages:</b> <code>{messages_viewable}</code>\n</blockquote>"
    if messages_sent:
        caption += f"<blockquote>💬 <b>Messages sent:</b> <code>{messages_sent}</code>\n</blockquote>"
    elif messages_sent_alt:
        caption += f<blockquote>"💬 <b>Messages sent:</b> <code>{messages_sent_alt}</code> ⚠\n</blockquote>"
    if members is not None:
        caption += f"<blockquote>👥 <b>Members:</b> <code>{members}</code>\n</blockquote>"
    if admins:
        caption += f"<blockquote>👮 <b>Administrators:</b> <code>{admins}</code>\n</blockquote>"
    if full.bot_info:
        caption += f"<blockquote>🤖 <b>Bots:</b> <code>{len(full.bot_info)}</code>\n</blockquote>"
    if members_online:
        caption += f"<blockquote>👀 <b>Currently online:</b> <code>{members_online}</code>\n</blockquote>"
    if restricted_users is not None:
        caption += f"<blockquote>🔕 <b>Restricted users:</b> <code>{restricted_users}</code>\n</blockquote>"
    if banned_users:
        caption += f"<blockquote>📨 <b>Banned users:</b> <code>{banned_users}</code>\n</blockquote>"
    if group_stickers:
        caption += f'<blockquote>📹 <b>{chat_type} stickers:</b> <a href="t.me/addstickers/{full.stickerset.short_name}">{group_stickers}</a>\n</blockquote>'
    if not broadcast:
        if getattr(chat, "slowmode_enabled", None):
            caption += f"<blockquote>👉 <b>Slow mode:</b> <code>True</code>"
            caption += f", 🕐 <code>{full.slowmode_seconds}s</code>\n</blockquote>"
        else:
            caption += f"<blockquote>🦸‍♂ <b>Supergroup:</b> {supergroup}\n</blockquote>"
    if getattr(chat, "restricted", None):
        caption += f"<blockquote>🎌 <b>Restricted:</b> {chat.restricted}\n</blockquote>"
        rist = chat.restriction_reason[0]
        caption += f"<blockquote>> Platform: {rist.platform}\n</blockquote>"
        caption += f"<blockquote>> Reason: {rist.reason}\n</blockquote>"
        caption += f"<blockquote>> Text: {rist.text}\n\n</blockquote>"
    if getattr(chat, "scam", None):
        caption += "<blockquote>⚠ <b>Scam:</b> <b>Yes</b>\n</blockquote>"
    if getattr(chat, "verified", None):
        caption += f"<blockquote>✅ <b>Verified by Telegram:</b> <code>Yes</code>\n\n</blockquote>"
    if full.about:
        caption += f"<blockquote>🗒 <b>Description:</b> \n<code>{full.about}</code>\n</blockquote>"
    return chat_photo, caption
