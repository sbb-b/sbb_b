import os
from pathlib import Path

from ..Config import Config
from ..utils import load_module, remove_plugin
from . import CMD_HELP, CMD_LIST, SUDO_LIST, edit_delete, edit_or_reply, sbb_b

DELETE_TIMEOUT = 5
thumb_image_path = os.path.join(Config.TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")


@sbb_b.ar_cmd(pattern="تنصيب$")
async def install(event):
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(
                await event.get_reply_message(),
                "sbb_b/plugins/",
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await edit_delete(
                    event,
                    f"- تم تنصيب الملف `{os.path.basename(downloaded_file_name)}`",
                    10,
                )
            else:
                os.remove(downloaded_file_name)
                await edit_delete(
                    event, "**خـطأ اسم هذا الملـف موجود بالفعل في السورس**.", 10
                )
        except Exception as e:
            await edit_delete(event, f"**خـطأ:**\n`{e}`", 20)
            os.remove(downloaded_file_name)


@sbb_b.ar_cmd(pattern="الغاء تنصيب ([\s\S]*)")
async def unload(event):
    shortname = event.pattern_match.group(1)
    path = Path(f"sbb_b/plugins/{shortname}.py")
    if not os.path.exists(path):
        return await edit_delete(
            event, f"لا يوجد اسم ملف مع المسار {path} لألغاء تنصيبه"
        )
    os.remove(path)
    if shortname in CMD_LIST:
        CMD_LIST.pop(shortname)
    if shortname in SUDO_LIST:
        SUDO_LIST.pop(shortname)
    if shortname in CMD_HELP:
        CMD_HELP.pop(shortname)
    try:
        remove_plugin(shortname)
        await edit_or_reply(event, f"{shortname} تم بنجاح الغاء تنصيبه")
    except Exception as e:
        await edit_or_reply(event, f"تم بنجاح الغاء تنصيب {shortname}\n{e}")
