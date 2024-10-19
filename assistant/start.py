# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.

from datetime import datetime

from pytz import timezone as tz
from telethon import Button, events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.utils import get_display_name

from pyUltroid._misc import SUDO_M, owner_and_sudos
from pyUltroid.dB.base import KeyManager
from pyUltroid.fns.helper import inline_mention
from strings import get_string

from . import *

Owner_info_msg = udB.get_key("BOT_INFO_START")
custom_info = True
if Owner_info_msg is None:
    custom_info = """
<pre><code>
Tʜɪs Is Tʜᴇ Bᴏᴛ Oғ @RemainsAlways
Aɴ PᴏᴡᴇʀFᴜʟʟ Usᴇʀʙᴏᴛ 
</pre></code>
"""
    Owner_info_msg = f"""
<pre><code>
<b>Owner</b> - {OWNER_NAME}
<b>OwnerID</b> - `{OWNER_ID}`

<b>Message Forwards</b> - {udB.get_key("PMBOT")}

<b>Ultroid [v{ultroid_version}](https://github.com/TeamUltroid/Ultroid), powered by @TeamUltroid</b>
</pre></code>
"""


_settings = [
    [
        Button.inline("API Kᴇʏs", data="cbs_apiset"),
        Button.inline("Pᴍ Bᴏᴛ", data="cbs_chatbot"),
    ],
    [
        Button.inline("Aʟɪᴠᴇ", data="cbs_alvcstm"),
        Button.inline("PᴍPᴇʀᴍɪᴛ", data="cbs_ppmset"),
    ],
    [
        Button.inline("Fᴇᴀᴛᴜʀᴇs", data="cbs_otvars"),
        Button.inline("VC Sᴏɴɢ Bᴏᴛ", data="cbs_vcb"),
    ],
    [Button.inline("« Bᴀᴄᴋ", data="mainmenu")],
]

_start = [
    [
        Button.inline("Lᴀɴɢᴜᴀɢᴇ 🌐", data="lang"),
        Button.inline("Sᴇᴛᴛɪɴɢs ⚙️", data="setter"),
    ],
    [
        Button.inline("Sᴛᴀᴛs ✨", data="stat"),
        Button.inline("Bʀᴏᴀᴅᴄᴀsᴛ 📻", data="bcast"),
    ],
    [Button.inline("TɪᴍᴇZᴏɴᴇ 🌎", data="tz")],
]


@callback("ownerinfo")
async def own(event):
    msg = Owner_info_msg.format(
        mention=inline_mention(event.sender), me=inline_mention(ultroid_bot.me)
    )
    if custom_info:
        msg += "<blockquote>\n\n• Powered by @RemainsAlways</blockquote>"
    await event.edit(
        msg,
        buttons=[Button.inline("Close", data="closeit")],
        link_preview=False,
        parse_mode="html"
    )


@callback("closeit")
async def closet(lol):
    try:
        await lol.delete()
    except MessageDeleteForbiddenError:
        await lol.answer("MESSAGE_TOO_OLD", alert=True)


@asst_cmd(pattern="start( (.*)|$)", forwards=False, func=lambda x: not x.is_group)
async def ultroid(event):
    args = event.pattern_match.group(1).strip()
    keym = KeyManager("BOT_USERS", cast=list)
    if not keym.contains(event.sender_id) and event.sender_id not in owner_and_sudos():
        keym.add(event.sender_id)
        kak_uiw = udB.get_key("OFF_START_LOG")
        if not kak_uiw or kak_uiw != True:
            msg = f"<blockquote><i><b>{inline_mention(event.sender)} <code>[{event.sender_id}]</code> started your [Assistant bot](@{asst.me.username}).</blockquote></i></b>"
            buttons = [[Button.inline("Info", "itkkstyo")]]
            if event.sender.username:
                buttons[0].append(
                    Button.mention(
                        "User", await event.client.get_input_entity(event.sender_id)
                    )
                )
            await event.client.send_message(
                udB.get_key("LOG_CHANNEL"), msg, buttons=buttons, parse_mode="html"
            )
    if event.sender_id not in SUDO_M.fullsudos:
        ok = ""
        me = inline_mention(ultroid_bot.me)
        mention = inline_mention(event.sender)
        if args and args != "set":
            await get_stored_file(event, args)
        if not udB.get_key("STARTMSG"):
            if udB.get_key("PMBOT"):
                ok = "<blockquote><i><b>Mʏ Mᴀsᴛᴇʀ Is Tᴏᴏ Bᴜsʏ Tᴏ Cᴏɴᴛᴀᴄᴛ Wɪᴛʜ Eᴠᴇʀʏᴏɴᴇ!!\n\nSᴏ Tʜᴀᴛs Wʜʏ Mᴀsᴛᴇʀ Assɪɢɴᴇᴅ Mᴇ As Mᴀɴᴀɢᴇʀ. Sᴇɴᴅ Yᴏᴜʀ Mᴇssᴀɢᴇ Hᴇʀᴇ Aɴᴅ I Wɪʟʟ Fᴏʀᴡᴀʀᴅ Iᴛ Tᴏ Mʏ Mᴀsᴛᴇʀ's Dᴍ.</blockquote></i></b>"
            await event.reply(
                f"<blockquote><i><b>Hᴇʏ!! {mention}, Tʜɪs Is Tʜᴇ Mᴀɴᴀɢᴇʀ Oғ {me}!\n\n{ok}</blockquote></i></b>",
                parse_mode="html"
                file=udB.get_key("STARTMEDIA"),
                buttons=[Button.inline("Info.", data="ownerinfo")]
                if Owner_info_msg
                else None,
            )
        else:
            await event.reply(
                udB.get_key("STARTMSG").format(me=me, mention=mention),
                file=udB.get_key("STARTMEDIA"),
                buttons=[Button.inline("Info.", data="ownerinfo")]
                if Owner_info_msg
                else None,
            )
    else:
        name = get_display_name(event.sender)
        if args == "set":
            await event.reply(
                "Cʜᴏᴏsᴇ Fʀᴏᴍ Bᴇʟᴏᴡ Oᴘᴛɪᴏɴs -",
                buttons=_settings,
            )
        elif args:
            await get_stored_file(event, args)
        else:
            await event.reply(f"""<blockquote>
                {get_string("ast_3").format(name)}</blockquote>""",
                buttons=_start,
                parse_mode="html"
            )


@callback("itkkstyo", owner=True)
async def ekekdhdb(e):
    text = f"Wʜᴇɴ Usᴇʀs Wɪʟʟ Sᴛᴀʀᴛs Yᴏᴜʀ Bᴏᴛ Tʜᴇɴ Tʜᴇʏ Wɪʟʟ Sᴇᴇ Tʜɪs Sᴛᴀʀᴛ Mᴇssᴀɢᴇ.\n\nTᴏ Dɪsᴀʙʟᴇ : {HNDLR}setdb OFF_START_LOG True"
    await e.answer(text, alert=True)


@callback("mainmenu", owner=True, func=lambda x: not x.is_group)
async def ultroid(event):
    await event.edit(f"""<blockquote>
        {get_string("ast_3").format(OWNER_NAME)}</blockquote>""",
        buttons=_start,
    )


@callback("stat", owner=True)
async def botstat(event):
    ok = len(udB.get_key("BOT_USERS") or [])
    msg = """Uʟᴛʀᴏɪᴅ Mᴀɴᴀɢᴇʀ - Sᴛᴀᴛs
Tᴏᴛᴀʟ Usᴇʀs - {}""".format(
        ok,
    )
    await event.answer(msg, cache_time=0, alert=True)


@callback("bcast", owner=True)
async def bdcast(event):
    keym = KeyManager("BOT_USERS", cast=list)
    total = keym.count()
    await event.edit(f"<blockquote>• BʀᴏᴀᴅCᴀsᴛ Tᴏ {total} Usᴇʀs.</blockquote>", parse_mode="html")
    async with event.client.conversation(OWNER_ID) as conv:
        await conv.send_message(
            "<blockquote>Eɴᴛᴇʀ Yᴏᴜʀ BʀᴏᴀᴅCᴀsᴛ Mᴇssᴀɢᴇ.\nWᴀɴᴛ Tᴏ Cᴀɴᴄʟᴇ ? Sᴇɴᴅ /cancel</blockquote>",
            parse_mode="html"
        )
        response = await conv.get_response()
        if response.message == "/cancel":
            return await conv.send_message("Cᴀɴᴄʟʟᴇᴅ!!")
        success = 0
        fail = 0
        await conv.send_message(f"```Sᴛᴀʀᴛɪɴɢ BʀᴏᴀᴅCᴀsᴛ Tᴏ {total} Usᴇʀs...```")
        start = datetime.now()
        for i in keym.get():
            try:
                await asst.send_message(int(i), response)
                success += 1
            except BaseException:
                fail += 1
        end = datetime.now()
        time_taken = (end - start).seconds
        await conv.send_message(
            f"""<blockquote>
**BᴏʀᴀᴅCᴀsᴛ Cᴏᴍᴘʟɪᴛᴇᴅ Iɴ {time_taken} Sᴇᴄᴏɴᴅs.**
Tᴏᴛᴀʟ Usᴇʀs Iɴ Bᴏᴛ - {total}
**Sᴇɴᴛ Tᴏ** : `{success} Usᴇʀs.`
**Fᴀɪʟᴇᴅ Fᴏʀ** : `{fail} Usᴇʀs.`</blockquote>""", parse_mode="html"
        )


@callback("setter", owner=True)
async def setting(event):
    await event.edit(
        "<blockquote>Cʜᴏᴏsᴇ Fʀᴏᴍ Bᴇʟᴏᴡ Oᴘᴛɪᴏɴs -</blockquote>",
        buttons=_settings,
        parse_mode="html"
    )


@callback("tz", owner=True)
async def timezone_(event):
    await event.delete()
    pru = event.sender_id
    var = "TIMEZONE"
    name = "Timezone"
    async with event.client.conversation(pru) as conv:
        await conv.send_message(
            "<blockquote>Sᴇɴᴅ Yᴏᴜʀ TɪᴍᴇZᴏɴᴇ, Dᴏɴᴛ Kɴᴏᴡ ?  [Cʟɪᴄᴋ Hᴇʀᴇ!](http://www.timezoneconverter.com/cgi-bin/findzone.tzc)</blockquote>"
            , parse_mode="html"
        )
        response = conv.wait_event(events.NewMessage(chats=pru))
        response = await response
        themssg = response.message.message
        if themssg == "/cancel":
            return await conv.send_message(
                "Cᴀɴᴄʟʟᴇᴅ!!",
                buttons=get_back_button("mainmenu"),
            )
        try:
            tz(themssg)
            await setit(event, var, themssg)
            await conv.send_message(
                f"<blockquote>{name} Cʜᴀɴɢᴇᴅ Tᴏ {themssg}\n</blockquote>",
                buttons=get_back_button("mainmenu"),
                parse_mode="html"
            )
        except BaseException:
            await conv.send_message(
                "<blockquote>Wʀᴏɴɢ TɪᴍᴇZᴏɴᴇ, Tʀʏ Aɢᴀɪɴ</blockquote>",
                buttons=get_back_button("mainmenu"), parse_mode="html"
            )
