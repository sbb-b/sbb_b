import os

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl import functions
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import Channel, Chat, InputPhoto, User

from sbb_b import sbb_b

from ..Config import Config
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)


# ====================== CONSTANT ===============================
INVALID_MEDIA = "⌔∮ امتداد الصورة غير صالح."
PP_CHANGED = "⌔∮ تم تغيير صورة الملف الشخصي بنجاح."
PP_TOO_SMOL = "⌔∮ هذه الصورة صغيرة جدًا ، استخدم صورة أكبر."
PP_ERROR = "⌔∮ حدث فشل أثناء معالجة الصورة."
BIO_SUCCESS = "⌔∮ تم تغيير البايو بنجاح."
NAME_OK = "⌔∮ تم تغيير اسمك بنجاح."
USERNAME_SUCCESS = "⌔∮ تم تغيير اسم المستخدم الخاص بك بنجاح."
USERNAME_TAKEN = "⌔∮ أسم المستخدم مأخوذ مسبقا."
# ===============================================================


@sbb_b.ar_cmd(pattern="تغيير بايو ([\s\S]*)")
async def _(event):
    bio = event.pattern_match.group(1)
    try:
        await event.client(functions.account.UpdateProfileRequest(about=bio))
        await edit_delete(event, "تم بنجاح تغيير البايو الخاص بي")
    except Exception as e:
        await edit_or_reply(event, f"**خطأ:**\n{e}")


@sbb_b.ar_cmd(pattern="تغيير اسم ([\s\S]*)")
async def _(event):
    names = event.pattern_match.group(1)
    first_name = names
    last_name = ""
    if ";" in names:
        first_name, last_name = names.split(";", 1)
    try:
        await event.client(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await edit_delete(event, "تم بنجاح تغيير الاسم الخاص بي")
    except Exception as e:
        await edit_or_reply(event, f"**خطأ:**\n{e}")


@sbb_b.ar_cmd(pattern="تغيير صورة$")
async def _(event):
    reply_message = await event.get_reply_message()
    sbb_bevent = await edit_or_reply(event, "يتم تحميل الصورة لحسابي ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await event.client.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as e:
        await sbb_bevent.edit(str(e))
    else:
        if photo:
            await sbb_bevent.edit("**⌔∮ الان يتم التحميل الى تيليكرام ...**")
            if photo.endswith((".mp4", ".MP4")):
                size = os.stat(photo).st_size
                if size > 2097152:
                    await sbb_bevent.edit("⌔∮ الحجم يجب ان يكون اقل من 2 ميغا")
                    os.remove(photo)
                    return
                sbb_bpic = None
                sbb_bvideo = await event.client.upload_file(photo)
            else:
                sbb_bpic = await event.client.upload_file(photo)
                sbb_bvideo = None
            try:
                await event.client(
                    functions.photos.UploadProfilePhotoRequest(
                        file=sbb_bpic, video=sbb_bvideo, video_start_ts=0.01
                    )
                )
            except Exception as e:
                await sbb_bevent.edit(f"**خطأ:**\n{e}")
            else:
                await edit_or_reply(sbb_bevent, "**❃ تم بنجاح تغيير صورة الحساب**")
    try:
        os.remove(photo)
    except Exception as e:
        LOGS.info(str(e))


@sbb_b.ar_cmd(pattern="تغيير معرف ([\s\S]*)")
async def update_username(event):
    newusername = event.pattern_match.group(1)
    try:
        await event.client(UpdateUsernameRequest(newusername))
        await edit_delete(event, USERNAME_SUCCESS)
    except UsernameOccupiedError:
        await edit_or_reply(event, USERNAME_TAKEN)
    except Exception as e:
        await edit_or_reply(event, f"**خطأ:**\n{e}")


@sbb_b.ar_cmd(pattern="حسابي$")
async def count(event):
    u = 0
    g = 0
    c = 0
    bc = 0
    b = 0
    result = ""
    sbb_bevent = await edit_or_reply(event, "**⌔∮ يتم جمع معلومات حسابك**")
    dialogs = await event.client.get_dialogs(limit=None, ignore_migrated=True)
    for d in dialogs:
        currrent_entity = d.entity
        if isinstance(currrent_entity, User):
            if currrent_entity.bot:
                b += 1
            else:
                u += 1
        elif isinstance(currrent_entity, Chat):
            g += 1
        elif isinstance(currrent_entity, Channel):
            if currrent_entity.broadcast:
                bc += 1
            else:
                c += 1
        else:
            LOGS.info(d)

    result += f"⪼ المستخدمين:\t**{u}**\n"
    result += f"⪼ المجموعات:\t**{g}**\n"
    result += f"⪼ المجموعات الخارقة:\t**{c}**\n"
    result += f"⪼ القنوات:\t**{bc}**\n"
    result += f"⪼ البوتات:\t**{b}**"

    await sbb_bevent.edit(result)


@sbb_b.ar_cmd(pattern="ازاله الصورة ?([\s\S]*)")
async def remove_profilepic(delpfp):
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = [
        InputPhoto(
            id=sep.id,
            access_hash=sep.access_hash,
            file_reference=sep.file_reference,
        )
        for sep in pfplist.photos
    ]
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await edit_delete(delpfp, f"**⪼ تم بنجاح حذف {len(input_photos)} صورة الحساب**")


@sbb_b.ar_cmd(pattern="معرفاتي$")
async def _(event):
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "**⌔∮ المعرفات الموجودة لدي هي:**\n"
    output_str += "".join(
        f" ⪼ {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await edit_or_reply(event, output_str)
