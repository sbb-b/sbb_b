import os
from typing import Optional

from moviepy.editor import VideoFileClip
from PIL import Image

from ...core.logger import logging
from ...core.managers import edit_or_reply
from ..tools import media_type
from .utils import runcmd

LOGS = logging.getLogger(__name__)


async def media_to_pic(event, reply, noedits=False):  # sourcery no-metrics
    mediatype = media_type(reply)
    if mediatype not in [
        "Photo",
        "Round Video",
        "Gif",
        "Sticker",
        "Video",
        "Voice",
        "Audio",
        "Document",
    ]:
        return event, None
    if not noedits:
        sbb_bevent = await edit_or_reply(
            event, "**⎙ :: جاري التحويل انتظر قليلا  ** ...."
        )

    else:
        sbb_bevent = event
    sbb_bmedia = None
    sbb_bfile = os.path.join("./temp/", "meme.png")
    if os.path.exists(sbb_bfile):
        os.remove(sbb_bfile)
    if mediatype == "Photo":
        sbb_bmedia = await reply.download_media(file="./temp")
        im = Image.open(sbb_bmedia)
        im.save(sbb_bfile)
    elif mediatype in ["Audio", "Voice"]:
        await event.client.download_media(reply, sbb_bfile, thumb=-1)
    elif mediatype == "Sticker":
        sbb_bmedia = await reply.download_media(file="./temp")
        if sbb_bmedia.endswith(".tgs"):
            sbb_bcmd = f"lottie_convert.py --frame 0 -if lottie -of png '{sbb_bmedia}' '{sbb_bfile}'"
            stdout, stderr = (await runcmd(sbb_bcmd))[:2]
            if stderr:
                LOGS.info(stdout + stderr)
        elif sbb_bmedia.endswith(".webp"):
            im = Image.open(sbb_bmedia)
            im.save(sbb_bfile)
    elif mediatype in ["Round Video", "Video", "Gif"]:
        await event.client.download_media(reply, sbb_bfile, thumb=-1)
        if not os.path.exists(sbb_bfile):
            sbb_bmedia = await reply.download_media(file="./temp")
            clip = VideoFileClip(media)
            try:
                clip = clip.save_frame(sbb_bfile, 0.1)
            except Exception:
                clip = clip.save_frame(sbb_bfile, 0)
    elif mediatype == "Document":
        mimetype = reply.document.mime_type
        mtype = mimetype.split("/")
        if mtype[0].lower() == "image":
            sbb_bmedia = await reply.download_media(file="./temp")
            im = Image.open(sbb_bmedia)
            im.save(sbb_bfile)
    if sbb_bmedia and os.path.lexists(sbb_bmedia):
        os.remove(sbb_bmedia)
    if os.path.lexists(sbb_bfile):
        return sbb_bevent, sbb_bfile, mediatype
    return sbb_bevent, None


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    thumb_image_path = path or os.path.join(
        "./temp/", f"{os.path.basename(video_file)}.jpg"
    )
    command = f"ffmpeg -ss {duration} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        LOGS.error(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
