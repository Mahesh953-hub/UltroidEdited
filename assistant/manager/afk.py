# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from datetime import datetime as dt

from telethon.events import NewMessage
from telethon.tl.types import (
    Message,
    MessageEntityMention,
    MessageEntityMentionName,
    User,
)
from telethon.utils import get_display_name

from pyUltroid.fns.helper import inline_mention, time_formatter

from . import asst, asst_cmd

AFK = {}


@asst_cmd(pattern="afk", func=lambda x: not x.is_private)
async def go_afk(event):
    sender = await event.get_sender()
    if (not isinstance(sender, User)) or sender.bot:
        return
    try:
        reason = event.text.split(" ", maxsplit=1)[1]
    except IndexError:
        reason = None
    if event.is_reply and not reason:
        replied = await event.get_reply_message()
        if not reason and replied.text and not replied.media:
            reason = replied.text
        else:
            reason = replied
    time_ = dt.now()
    if AFK.get(event.chat_id):
        AFK[event.chat_id].update({event.sender_id: {"reason": reason, "time": time_}})
    else:
        AFK.update(
            {event.chat_id: {event.sender_id: {"reason": reason, "time": time_}}}
        )
    mention = inline_mention(sender)
    msg = f"<blockquote><i><b>{mention} went AFK Now!</blockquote></i></b>"
    if reason and not isinstance(reason, str):
        await event.reply(reason)
    else:
        msg += f"<blockquote><i><b>\n\nReason :  {reason}</blockquote></i></b>"
    await event.reply(msg, parse_mode="html")


@asst.on(NewMessage(func=lambda x: AFK.get(x.chat_id) and not x.is_private))
async def make_change(event):
    if event.text.startswith("/afk"):
        return
    sender = await event.get_sender()
    if (not isinstance(sender, User)) or sender.bot:
        return
    chat_ = AFK[event.chat_id]
    if event.sender_id in chat_.keys():
        name = get_display_name(event.sender)
        cha_send = chat_[event.sender_id]
        time_ = time_formatter((dt.now() - cha_send["time"]).seconds * 1000)
        msg = f"<blockquote><i><b>{name} Jaldi Wapis Aagya!\n AFK for {time_}</blockquote></i></b>"
        await event.reply(msg, parse_mode="html")
        del chat_[event.sender_id]
        if not chat_:
            del AFK[event.chat_id]
    ST_SPAM = []
    replied = await event.get_reply_message()
    if replied:
        name = get_display_name(replied.sender)
        if replied.sender_id in chat_.keys():
            s_der = chat_[replied.sender_id]
            res_ = s_der["reason"]
            time_ = time_formatter((dt.now() - s_der["time"]).seconds * 1000)
            msg = f"<blockquote><i><b>{name} is AFK Currently!\nFrom : {time_}</blockquote></i></b>"
            if res_ and isinstance(res_, str):
                msg += f"<blockquote><i><b>\nReason : {res_}</blockquote></i></b>"
            elif res_ and isinstance(res_, Message):
                await event.reply(res_, parse_mode="html")
            await event.reply(msg, parse_mode="html")
        ST_SPAM.append(replied.sender_id)
    for ent, text in event.get_entities_text():
        dont_send, entity = None, None
        if isinstance(ent, MessageEntityMentionName):
            c_id = ent.user_id
        elif isinstance(ent, MessageEntityMention):
            c_id = text
        else:
            c_id = None
        if c_id:
            entity = await event.client.get_entity(c_id)
        if entity and entity.id in chat_.keys() and entity.id not in ST_SPAM:
            ST_SPAM.append(entity.id)
            s_der = chat_[entity.id]
            name = get_display_name(entity)
            res_ = s_der["reason"]
            time_ = time_formatter((dt.now() - s_der["time"]).seconds * 1000)
            msg = f"<blockquote><i><b>{name} So Rha Hai!\nPichle : {time_} se.</blockquote></i></b>"
            if res_ and isinstance(res_, str):
                msg += f"<blockquote><i><b>\nReason : {res_}</blockquote></i></b>"
            elif res_ and isinstance(res_, Message):
                await event.reply(res_, parse_mode="html")
            await event.reply(msg, parse_mode="html")
