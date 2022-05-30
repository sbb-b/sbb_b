# sbb_b module for purging unneeded messages(usually spam or ot).
import re
from asyncio import sleep

from telethon.errors import rpcbaseerrors
from telethon.tl.types import (
    InputMessagesFilterDocument,
    InputMessagesFilterEmpty,
    InputMessagesFilterGeo,
    InputMessagesFilterGif,
    InputMessagesFilterMusic,
    InputMessagesFilterPhotos,
    InputMessagesFilterRoundVideo,
    InputMessagesFilterUrl,
    InputMessagesFilterVideo,
    InputMessagesFilterVoice,
)

from sbb_b import sbb_b

from ..core.managers import edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

purgelist = {}

purgetype = {
    "ب": InputMessagesFilterVoice,
    "م": InputMessagesFilterDocument,
    "ح": InputMessagesFilterGif,
    "ص": InputMessagesFilterPhotos,
    "l": InputMessagesFilterGeo,
    "غ": InputMessagesFilterMusic,
    "r": InputMessagesFilterRoundVideo,
    "ق": InputMessagesFilterEmpty,
    "ر": InputMessagesFilterUrl,
    "ف": InputMessagesFilterVideo,
    # "ك": search
}


@sbb_b.ar_cmd(pattern="مسح(\s*| \d+)$")
async def delete_it(event):
    input_str = event.pattern_match.group(1).strip()
    msg_src = await event.get_reply_message()
    if msg_src:
        if input_str and input_str.isnumeric():
            await event.delete()
            await sleep(int(input_str))
            try:
                await msg_src.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#الـمسـح \n ⌯︙تـم حـذف الـرسالة بـنجاح"
                    )
            except rpcbaseerrors.BadRequestError:
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        "⌯︙لا يمـكنني الـحذف احـتاج صلاحيـات الادمـن",
                    )
        elif input_str:
            if not input_str.startswith("var"):
                await edit_or_reply(event, "⌯︙عـذرا الـرسالة غيـر موجـودة")
        else:
            try:
                await msg_src.delete()
                await event.delete()
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID, "#الـمسـح \n ⌯︙تـم حـذف الـرسالة بـنجاح"
                    )
            except rpcbaseerrors.BadRequestError:
                await edit_or_reply(event, "⌯︙عـذرا الـرسالة لا استـطيع حـذفها")
    elif not input_str:
        await event.delete()


@sbb_b.ar_cmd(pattern="حذف رسائلي")
async def purgeme(event):
    message = event.text
    count = int(message[12:])
    i = 1
    async for message in event.client.iter_messages(event.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await event.client.send_message(
        event.chat_id,
        f"**▾∮ تم حذف** " + str(count) + " رساله ",
    )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#حذف_الرسائل \n`تم حذف" + str(count) + " رساله بنجاح.`",
        )
    await sleep(5)
    await smsg.delete()


# TODO: only sticker messages.
@sbb_b.ar_cmd(pattern="تنظيف(?:\s|$)([\s\S]*)")
async def fastpurger(event):
    chat = await event.get_input_chat()
    msgs = []
    count = 0
    input_str = event.pattern_match.group(1)
    ptype = re.findall(r"-\w+", input_str)
    try:
        p_type = ptype[0].replace("-", "")
        input_str = input_str.replace(ptype[0], "").strip()
    except IndexError:
        p_type = None
    error = ""
    result = ""
    await event.delete()
    reply = await event.get_reply_message()
    if reply:
        if input_str and input_str.isnumeric():
            if p_type is not None:
                for ty in p_type:
                    if ty in purgetype:
                        async for msg in event.client.iter_messages(
                            event.chat_id,
                            limit=int(input_str),
                            offset_id=reply.id - 1,
                            reverse=True,
                            filter=purgetype[ty],
                        ):
                            count += 1
                            msgs.append(msg)
                            if len(msgs) == 50:
                                await event.client.delete_messages(chat, msgs)
                                msgs = []
                        if msgs:
                            await event.client.delete_messages(chat, msgs)
                    elif ty == "كلمه":
                        error += f"\n⌯︙الاضافه خـطأ"
                    else:
                        error += f"\n\n⌯︙`{ty}`  : هـذه أضافـة خاطئـة "
            else:
                count += 1
                async for msg in event.client.iter_messages(
                    event.chat_id,
                    limit=(int(input_str) - 1),
                    offset_id=reply.id,
                    reverse=True,
                ):
                    msgs.append(msg)
                    count += 1
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
        elif input_str and p_type is not None:
            if p_type == "كلمه":
                try:
                    cont, inputstr = input_str.split(" ")
                except ValueError:
                    cont = "error"
                    inputstr = input_str
                cont = cont.strip()
                inputstr = inputstr.strip()
                if cont.isnumeric():
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        limit=int(cont),
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=inputstr,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                else:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        offset_id=reply.id - 1,
                        reverse=True,
                        search=input_str,
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            else:
                error += f"\n⌯︙`{ty}`  : هـذه أضافـة خاطئـة "
        elif input_str:
            error += f"\n⌯︙`.تنظيف {input_str}` الامـر خـطأ يـرجى الكتابة بـشكل صحيح"
        elif p_type is not None:
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id,
                        min_id=event.reply_to_msg_id - 1,
                        filter=purgetype[ty],
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                else:
                    error += f"\n⌯︙`{ty}`  : هـذه أضافـة خاطئـة"
        else:
            async for msg in event.client.iter_messages(
                chat, min_id=event.reply_to_msg_id - 1
            ):
                count += 1
                msgs.append(msg)
                if len(msgs) == 50:
                    await event.client.delete_messages(chat, msgs)
                    msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
    elif p_type is not None and input_str:
        if p_type != "كلمه" and input_str.isnumeric():
            for ty in p_type:
                if ty in purgetype:
                    async for msg in event.client.iter_messages(
                        event.chat_id, limit=int(input_str), filter=purgetype[ty]
                    ):
                        count += 1
                        msgs.append(msg)
                        if len(msgs) == 50:
                            await event.client.delete_messages(chat, msgs)
                            msgs = []
                    if msgs:
                        await event.client.delete_messages(chat, msgs)
                elif ty == "الكتابه":
                    error += f"\n⌯︙لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه"
                else:
                    error += f"\n⌯︙`{ty}`  : هـذه أضافـة خاطئـة "
        elif p_type == "كلمه":
            try:
                cont, inputstr = input_str.split(" ")
            except ValueError:
                cont = "error"
                inputstr = input_str
            cont = cont.strip()
            inputstr = inputstr.strip()
            if cont.isnumeric():
                async for msg in event.client.iter_messages(
                    event.chat_id, limit=int(cont), search=inputstr
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            else:
                async for msg in event.client.iter_messages(
                    event.chat_id, search=input_str
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
            if msgs:
                await event.client.delete_messages(chat, msgs)
        else:
            error += f"\n⌯︙`{ty}`  : هـذه أضافـة خاطئـة "
    elif p_type is not None:
        for ty in p_type:
            if ty in purgetype:
                async for msg in event.client.iter_messages(
                    event.chat_id, filter=purgetype[ty]
                ):
                    count += 1
                    msgs.append(msg)
                    if len(msgs) == 50:
                        await event.client.delete_messages(chat, msgs)
                        msgs = []
                if msgs:
                    await event.client.delete_messages(chat, msgs)
            elif ty == "كلمه":
                error += f"\n⌯︙لا تستطـيع استـخدام امر التنظيف عبر البحث مع الاضافه"
            else:
                error += f"\n⌯︙`{ty}`  : هـذه أضافـة خاطئـة "
    elif input_str.isnumeric():
        async for msg in event.client.iter_messages(chat, limit=int(input_str) + 1):
            count += 1
            msgs.append(msg)
            if len(msgs) == 50:
                await event.client.delete_messages(chat, msgs)
                msgs = []
        if msgs:
            await event.client.delete_messages(chat, msgs)
    else:
        error += "\n⌯︙لم يتـم تحـديد اضافـة يرجى ارسال  (`.اوامر التنظيف`) و رؤية اوامر التنظيف"
    if msgs:
        await event.client.delete_messages(chat, msgs)
    if count > 0:
        result += "⌯︙اكـتمل الـتنظيف السـريع\n⌯︙تـم حـذفㅤ" + str(count) + "ㅤمن الـرسائل"
    if error != "":
        result += f"\n\n**خـطأ:**{error}"
    if result == "":
        result += "⌯︙لا تـوجد رسـائل لـتنظيفها"
    hi = await event.client.send_message(event.chat_id, result)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#التنـظيف \n{result}",
        )
    await sleep(5)
    await hi.delete()
