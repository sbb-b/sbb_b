import json
import os
import re

from telethon.events import CallbackQuery

from sbb_b import sbb_b


@sbb_b.tgbot.on(CallbackQuery(data=re.compile(b"secret_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./sbb_b/secrets.txt"):
        jsondata = json.load(open("./sbb_b/secrets.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid, jmthon.uid]
            if event.query.user_id in ids:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
            else:
                reply_pop_up_alert = "عذرا هذه الرسالة ليست لك  !"
        except KeyError:
            reply_pop_up_alert = "لم تعد هذه الرسالة موجودة في سيرفر جمثون"
    else:
        reply_pop_up_alert = "هذه الرسالة لم تعد موجودة"
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
