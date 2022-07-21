import json
import os
import re

from telethon.events import CallbackQuery

from sbb_b import sbb_b


@sbb_b.tgbot.on(CallbackQuery(data=re.compile(b"troll_(.*)")))
async def on_plug_in_callback_query_handler(event):
    timestamp = int(event.pattern_match.group(1).decode("UTF-8"))
    if os.path.exists("./sbb_b/troll.txt"):
        jsondata = json.load(open("./sbb_b/troll.txt"))
        try:
            message = jsondata[f"{timestamp}"]
            userid = message["userid"]
            ids = [userid]
            if event.query.user_id in ids:
                reply_pop_up_alert = (
                    "عذرا لكن هذه المره ليست لك الرسالة حظا موفقا لاحقا"
                )
            else:
                encrypted_tcxt = message["text"]
                reply_pop_up_alert = encrypted_tcxt
        except KeyError:
            reply_pop_up_alert = "هذه الرسالة لم تعد موجودة في سيرفر السورس"
    else:
        reply_pop_up_alert = "هذه الرسالة لم تعد موجودة "
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
