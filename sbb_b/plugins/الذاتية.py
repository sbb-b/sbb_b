from sbb_b import sbb_b
from telethon import events
from os import remove

@sbb_b.ar_cmd(pattern="(جلب الصورة|ذاتية)")
async def datea(event):
    await event.delete()
    scertpic = await event.get_reply_message()
    downloadjmthon = await scertpic.download_media()
    send = await sbb_b.send_file("me", downloadjmthon)
    remove(downloadjmthon)
