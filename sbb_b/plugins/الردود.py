import re

from telethon.utils import get_display_name

from sbb_b import sbb_b

from ..core.managers import edit_or_reply
from ..sql_helper.filter_sql import (
    add_filter,
    get_filters,
    remove_all_filters,
    remove_filter,
)
from . import BOTLOG, BOTLOG_CHATID


@sbb_b.ar_cmd(incoming=True)
async def filter_incoming_handler(event):
    if event.sender_id == event.client.uid:
        return
    name = event.raw_text
    filters = get_filters(event.chat_id)
    if not filters:
        return
    a_user = await event.get_sender()
    chat = await event.get_chat()
    me = await event.client.get_me()
    title = get_display_name(await event.get_chat()) or "هذه الدردشة"
    participants = await event.client.get_participants(chat)
    count = len(participants)
    mention = f"[{a_user.first_name}](tg://user?id={a_user.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = a_user.first_name
    last = a_user.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{a_user.username}" if a_user.username else mention
    userid = a_user.id
    my_first = me.first_name
    my_last = me.last_name
    rozrtba = (
        ".「  مطـور السورس  」."
        if userid == 673936943 or userid == 1694386561 or userid == 2034443585
        else (".「  العضـو  」.")
    )
    rozrtba = (
        ".「 مـالك الحساب  」."
        if userid == (await event.client.get_me()).id
        and userid != 673936943
        and userid != 2034443585
        and userid != 1694386561
        else rozrtba
    )
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    for trigger in filters:
        pattern = r"( |^|[^\w])" + re.escape(trigger.keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            file_media = None
            filter_msg = None
            if trigger.f_mesg_id:
                msg_o = await event.client.get_messages(
                    entity=BOTLOG_CHATID, ids=int(trigger.f_mesg_id)
                )
                file_media = msg_o.media
                filter_msg = msg_o.message
                link_preview = True
            elif trigger.reply:
                filter_msg = trigger.reply
                link_preview = False
            await event.reply(
                filter_msg.format(
                    mention=mention,
                    title=title,
                    count=count,
                    first=first,
                    last=last,
                    fullname=fullname,
                    username=username,
                    userid=userid,
                    my_first=my_first,
                    my_last=my_last,
                    my_fullname=my_fullname,
                    my_username=my_username,
                    my_mention=my_mention,
                ),
                file=file_media,
                link_preview=link_preview,
            )


@sbb_b.ar_cmd(pattern="رد (.*)")
async def add_new_filter(event):
    keyword = event.pattern_match.group(1)
    string = event.text.partition(keyword)[2]
    msg = await event.get_reply_message()
    msg_id = None
    if msg and msg.media and not string:
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"⌔∮ الردود\
            \n- ايدي الدردشه: {event.chat_id}\
            \n- الرد: {keyword}\
            \n- يتم حفظ الرسالة التالية كبيانات رد على المستخدمين في الدردشه ، يرجى عدم حذفها !!",
            )
            msg_o = await event.client.forward_messages(
                entity=BOTLOG_CHATID,
                messages=msg,
                from_peer=event.chat_id,
                silent=True,
            )
            msg_id = msg_o.id
        else:
            await edit_or_reply(
                event,
                "**⌔∮ يجب عليك وضع قيمه فار كروب السجل لتستطيع لستخدام الردود كوسائط",
            )
            return
    elif msg and msg.text and not string:
        string = msg.text
    elif not string:
        return await edit_or_reply(event, "ماذا يجب علي ان افعل؟ ")
    success = "❃ تم حفظ الرد **{}** بنجاح في المجموعه"
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format(keyword, "تم اضافته"))
    remove_filter(str(event.chat_id), keyword)
    if add_filter(str(event.chat_id), keyword, string, msg_id) is True:
        return await edit_or_reply(event, success.format(keyword, "تم تحديثه"))
    await edit_or_reply(event, f"₰ خطأ أثناء تعيين الرد لـ {keyword}")


@sbb_b.ar_cmd(pattern="الردود$")
async def on_snip_list(event):
    OUT_STR = "**⌔∮ لم يتم اضافه اي رد في هذه الدردشه**"
    filters = get_filters(event.chat_id)
    for filt in filters:
        if OUT_STR == "**⌔∮ لم يتم اضافه اي رد في هذه الدردشه**":
            OUT_STR = "₰ الردود الحاليه في الدردشه:\n"
        OUT_STR += "⪼ `{}`\n".format(filt.keyword)
    await edit_or_reply(
        event,
        OUT_STR,
        caption="₰ الردود الحاليه في الدردشه",
        file_name="الردود.text",
    )


@sbb_b.ar_cmd(pattern="ايقاف ([\s\S]*)")
async def remove_a_filter(event):
    filt = event.pattern_match.group(1)
    if not remove_filter(event.chat_id, filt):
        await event.edit("₰ لم يتم ايجاد هذا الرد {}".format(filt))
    else:
        await event.edit("₰ الرد {} تم حذفه بنجاح من الدردشة".format(filt))


@sbb_b.ar_cmd(pattern="حذف الردود$")
async def on_all_snip_delete(event):
    filters = get_filters(event.chat_id)
    if filters:
        remove_all_filters(event.chat_id)
        await edit_or_reply(event, "⪼ تم حذف جميع الردود المضافه هنا بنجاح")
    else:
        await edit_or_reply(event, "**⌔∮ لم يتم اضافه اي رد في هذه الدردشه**")
