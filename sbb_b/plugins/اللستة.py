from telegraph import upload_file as uf
from telethon.tl.types import Message
from telethon.utils import pack_bot_file_id

from sbb_b.strings import create_tl_btn, get_msg_button
from sbb_b import LOGS, sbb_b
from sbb_b.Config import Config

from ..core.managers import edit_or_reply

roz = Config.TG_BOT_USERNAME

STUFF = {}


async def something(e, msg, media, button, reply=True, chat=None):
    if e.client._bot:
        return await e.reply(msg, file=media, buttons=button)
    num = len(STUFF) + 1
    STUFF.update({num: {"msg": msg, "media": media, "button": button}})
    try:
        res = await e.client.inline_query(roz, f"stf{num}")
        return await res[0].click(
            chat or e.chat_id,
            reply_to=bool(isinstance(e, Message) and reply),
            hide_via=True,
            silent=True,
        )

    except Exception as er:
        LOGS.exception(er)


@jmthon.ar_cmd(pattern="لستة ?(.*)")
async def butt(event):
    media, wut, text = None, None, None
    if event.reply_to:
        wt = await event.get_reply_message()
        if wt.text:
            text = wt.text
        if wt.media:
            wut = mediainfo(wt.media)
        if wut and wut.startswith(("pic", "gif")):
            dl = await wt.download_media()
            variable = uf(dl)
            media = "https://telegra.ph" + variable[0]
        elif wut == "video":
            if wt.media.document.size > 8 * 1000 * 1000:
                return await event.eor(get_string("com_4"), time=5)
            dl = await wt.download_media()
            variable = uf(dl)
            os.remove(dl)
            media = "https://telegra.ph" + variable[0]
        else:
            media = pack_bot_file_id(wt.media)
    try:
        text = event.text.split(maxsplit=1)[1]
    except IndexError:
        if not text:
            return await edit_or_reply(
                event,
                f"**⌔∮ يجب عليك كتابه الامر بالشكل الصحيح.**",
            )
    text, buttons = get_msg_button(text)
    if buttons:
        buttons = create_tl_btn(buttons)
    await something(event, text, media, buttons)
    await event.delete()
