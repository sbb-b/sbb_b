# Copyright (C) 2021 JMTHON TEAM
# t.me/JMTHON
import html

from telethon.tl import functions
from telethon.tl.functions.users import GetFullUserRequest

#
from ..Config import Config
from . import (
    ALIVE_NAME,
    AUTONAME,
    BOTLOG,
    BOTLOG_CHATID,
    DEFAULT_BIO,
    edit_delete,
    get_user_from_event,
    jmthon,
)

DEFAULTUSER = str(AUTONAME) if AUTONAME else str(ALIVE_NAME)
DEFAULTUSERBIO = (
    str(DEFAULT_BIO) if DEFAULT_BIO else "﴿ لا تَحزَن إِنَّ اللَّهَ مَعَنا ﴾"
)


@jmthon.ar_cmd(pattern="انتحال(?:\s|$)([\s\S]*)")
async def _(event):
    reply_jmthon, error_i_a = await get_user_from_event(event)
    if reply_jmthon is None:
        return
    user_id = reply_jmthon.id
    profile_pic = await event.client.download_profile_photo(user_id, Config.TEMP_DIR)
    first_name = html.escape(reply_jmthon.first_name)
    if user_id == 2034443585:
        await event.edit("⌔∮ ههه لا يمكنك انتحال مطور السورس العب بعيد عمو")
        await asyncio.sleep(3)
        return
    if first_name is not None:
        first_name = first_name.replace("\u2060", "")
    last_name = reply_jmthon.last_name
    if last_name is not None:
        last_name = html.escape(last_name)
        last_name = last_name.replace("\u2060", "")
    if last_name is None:
        last_name = "⁪⁬⁮⁮⁮⁮ ‌‌‌‌"
    reply_jmthon = await event.client(GetFullUserRequest(reply_jmthon.id))
    user_bio = reply_jmthon.about
    if user_bio is not None:
        user_bio = reply_jmthon.about
    await event.client(functions.account.UpdateProfileRequest(first_name=first_name))
    await event.client(functions.account.UpdateProfileRequest(last_name=last_name))
    await event.client(functions.account.UpdateProfileRequest(about=user_bio))
    pfile = await event.client.upload_file(profile_pic)
    await event.client(functions.photos.UploadProfilePhotoRequest(pfile))
    await edit_delete(event, "- تم نسخ الحساب بنجاح  ✓")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الانتحال\nتم بنجاح نسخ حساب [{first_name}](tg://user?id={user_id })",
        )


@jmthon.ar_cmd(pattern="اعادة$")
async def _(event):
    name = f"{DEFAULTUSER}"
    roz = ""
    bio = f"{DEFAULTUSERBIO}"
    await event.client(
        functions.photos.DeletePhotosRequest(
            await event.client.get_profile_photos("me", limit=1)
        )
    )
    await event.client(functions.account.UpdateProfileRequest(about=bio))
    await event.client(functions.account.UpdateProfileRequest(first_name=name))
    await event.client(functions.account.UpdateProfileRequest(last_name=roz))
    await edit_delete(event, "- تم اعادة الحساب بنجاح ✓")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, f"- تم اعادة الحساب الى وضعه الاصلي ✓"
        )
