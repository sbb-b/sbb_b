from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events
import logging
import asyncio
from sbb_b import sbb_b
from ..core.session import tgbot
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)



@tgbot.on(events.NewMessage(pattern="^/men ?(.*)"))  #عفية اخمط يول
async def mentionall(event):
    if event.is_private:
        return await event.respond("- هذا الامر يستخدم فقط في المجموعات")
    admins = []
    async for admin in tgbot.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        admins.append(admin.id)
    if event.sender_id not in admins:
        return await event.respond("يجب ان تكون مشرف لاستخدام هذا الامر")
    if event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.reply_to_msg_id:
        mode = "text_on_reply"
        msg = event.reply_to_msg_id
        if msg is None:
            return await event.respond("- يجب ان تقوم بكتابه رسالة ححديدة لاستخدام الامر")
    elif event.pattern_match.group(1) and event.reply_to_msg_id:
        return await event.respond("يجب عليك كتابة رساله واحدة مع الامر")
    else:
        return await event.respond("عليك الرد على الرسالة او كتابتها مع الامر لعمل منشن")
    if mode == "text_on_cmd":
        usrnum = 0
        usrtxt = ""
        async for usr in tgbot.iter_participants(event.chat_id):
            usrnum += 1
            usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
            if usrnum == 5:
                await tgbot.send_message(event.chat_id, f"{usrtxt}\n\n{msg}")
                await asyncio.sleep(2)
                usrnum = 0
                usrtxt = ""
    if mode == "text_on_reply":
        usrnum = 0
        usrtxt = ""
        async for usr in tgbot.iter_participants(event.chat_id):
            usrnum += 1
            usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
            if usrnum == 5:
                await tgbot.send_message(event.chat_id, usrtxt, reply_to=msg)
                await asyncio.sleep(2)
                usrnum = 0
                usrtxt = ""
