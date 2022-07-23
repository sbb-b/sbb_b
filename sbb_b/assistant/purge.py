import asyncio

from telethon import events
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from telethon.tl.types import ChannelParticipantsAdmins

from sbb_b import sbb_b
from ..core.session import tgbot

OWNER_ID = sbb_b.uid
# حتى يتعرف من ان المستخدم مشرف
async def is_administrator(user_id: int, message):
    admin = False
    async for user in tgbot.iter_participants(
        message.chat_id, filter=ChannelParticipantsAdmins
    ):
        if user_id == user.id or OWNER_ID:
            admin = True
            break
    return admin


@tgbot.on(events.NewMessage(pattern="^تنظيف$"))
async def purge(event):
    chat = event.chat_id
    msgs = []

    if not await is_administrator(user_id=event.sender_id, message=event): # حتى يتاكد من كود الاشراف بسطر 12
        await event.reply("- يجب ان تكون مشرف اولا")
        return

    msg = await event.get_reply_message()
    if not msg: #حتى يتاكد انك سويت رد لرسالة
        await event.reply("يجب عليك الرد على الرسالة لحذف الرسائل التي تحتها")
        return

    try:
        msg_id = msg.id
        count = 0
        to_delete = event.message.id - 1
        await tgbot.delete_messages(chat, event.message.id)
        msgs.append(event.reply_to_msg_id)
        for m_id in range(to_delete, msg_id - 1, -1):
            msgs.append(m_id)
            count += 1
            if len(msgs) == 100:
                await tgbot.delete_messages(chat, msgs)
                msgs = []

        await tgbot.delete_messages(chat, msgs)
        del_res = await tgbot.send_message(
            event.chat_id, f"تم مسح {count} رسالة بنجاح ."
        )

        await asyncio.sleep(4)
        await del_res.delete()

    except MessageDeleteForbiddenError:
        text = (
            "فشل في حذف الرسائل\n"
            + "يبدو ان الرسائل قديمة جدا او انا لست مشرف"
        )
        del_res = await respond(text, parse_mode="md")
        await asyncio.sleep(5)
        await del_res.delete()

@tgbot.on(events.NewMessage(pattern="^مسح$"))
async def delete_msg(event):
    if not await is_administrator(user_id=event.sender_id, message=event):
        await event.reply("انت لست مشرف لاستخدام هذا الامر")
        return
    chat = event.chat_id
    msg = await event.get_reply_message()
    if not msg:
        await event.reply("يجب عليك الرد على الرسالة اولا")
        return
    to_delete = event.message
    chat = await event.get_input_chat()
    rm = [msg, to_delete]
    await tgbot.delete_messages(chat, rm)
