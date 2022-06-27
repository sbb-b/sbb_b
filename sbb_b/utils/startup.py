import asyncio
import glob
import os
import sys
from datetime import timedelta
from pathlib import Path

from telethon import Button, functions, types, utils
from telethon.tl.functions.channels import JoinChannelRequest

from sbb_b import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from ..Config import Config
from ..core.logger import logging
from ..core.session import sbb_b
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import (
    del_keyword_collectionlist,
    get_item_collectionlist,
)
from ..sql_helper.globals import addgvar, gvarstatus
from .pluginmanager import load_module
from .tools import create_supergroup

ENV = bool(os.environ.get("ENV", False))
LOGS = logging.getLogger("sbb_b")
cmdhr = Config.COMMAND_HAND_LER

if ENV:
    VPS_NOLOAD = ["vps"]
elif os.path.exists("config.py"):
    VPS_NOLOAD = ["heroku"]


bot = sbb_b
DEV = 2034443585


async def setup_bot():
    """
    To set up bot for sbb_b
    """
    try:
        await sbb_b.connect()
        config = await sbb_b(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == sbb_b.session.server_address:
                if sbb_b.session.dc_id != option.id:
                    LOGS.warning(
                        f"معرف DC ثابت في الجلسة من {sbb_b.session.dc_id}"
                        f" الى {option.id}"
                    )
                sbb_b.session.set_dc(option.id, option.ip_address, option.port)
                sbb_b.session.save()
                break
        bot_details = await sbb_b.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await sbb_b.start(bot_token=Config.TG_BOT_USERNAME)
        sbb_b.me = await sbb_b.get_me()
        sbb_b.uid = sbb_b.tgbot.uid = utils.get_peer_id(sbb_b.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(sbb_b.me)
    except Exception as e:
        LOGS.error(f"STRING_SESSION - {e}")
        sys.exit()


async def startupmessage():
    """
    Start up message in telegram logger group
    """
    try:
        if BOTLOG:
            Config.SBB_BLOGO = await sbb_b.tgbot.send_file(
                BOTLOG_CHATID,
                "https://telegra.ph/file/b81fe3118d5a1f987e6e2.jpg",
                caption="❃ عزيزي المستخدم تم تنصيب سورس جمثون لك بنجاح لمعرفه اوامر السورس؛ \n`.الاوامر`",
                buttons=[
                    (Button.url("مجموعة المساعده", "https://t.me/jmthon_support"),)
                ],
            )
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        msg_details = list(get_item_collectionlist("restart_update"))
        if msg_details:
            msg_details = msg_details[0]
    except Exception as e:
        LOGS.error(e)
        return None
    try:
        if msg_details:
            await sbb_b.check_testcases()
            message = await sbb_b.get_messages(msg_details[0], ids=msg_details[1])
            text = message.text + "\n\n₰ الان السورس شغال مره اخرى استمتع"
            await sbb_b.edit_message(msg_details[0], msg_details[1], text)
            if gvarstatus("restartupdate") is not None:
                await sbb_b.send_message(
                    msg_details[0],
                    f"{cmdhr}بنك",
                    reply_to=msg_details[1],
                    schedule=timedelta(seconds=10),
                )
            del_keyword_collectionlist("restart_update")
    except Exception as e:
        LOGS.error(e)
        return None


async def mybot():
    SBB_B_USER = bot.me.first_name
    The_razan = bot.uid
    rz_ment = f"[{SBB_B_USER}](tg://user?id={The_razan})"
    f"ـ {rz_ment}"
    f"⪼ هذا هو بوت خاص بـ {rz_ment} يمكنك التواصل معه هنا"
    starkbot = await sbb_b.tgbot.get_me()
    perf = "[ جمثون ]"
    bot_name = starkbot.first_name
    botname = f"@{starkbot.username}"
    if bot_name.endswith("Assistant"):
        print("تم تشغيل البوت")
    else:
        try:
            await bot.send_message("@BotFather", "/setinline")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", perf)
            await asyncio.sleep(2)
        except Exception as e:
            print(e)


async def add_bot_to_logger_group(chat_id):
    """
    To add bot to logger groups
    """
    bot_details = await sbb_b.tgbot.get_me()
    try:
        await sbb_b(
            functions.messages.AddChatUserRequest(
                chat_id=chat_id,
                user_id=bot_details.username,
                fwd_limit=1000000,
            )
        )
    except BaseException:
        try:
            await sbb_b(
                functions.channels.InviteToChannelRequest(
                    channel=chat_id,
                    users=[bot_details.username],
                )
            )
        except Exception as e:
            LOGS.error(str(e))


async def load_plugins(folder):
    """
    To load plugins from the mentioned folder
    """
    path = f"sbb_b/{folder}/*.py"
    files = glob.glob(path)
    files.sort()
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            try:
                if shortname.replace(".py", "") not in Config.NO_LOAD:
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(
                                shortname.replace(".py", ""),
                                plugin_path=f"sbb_b/{folder}",
                            )
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"sbb_b/{folder}/{shortname}.py"))
            except Exception as e:
                os.remove(Path(f"sbb_b/{folder}/{shortname}.py"))
                LOGS.info(f" لا يمكنني تحميل {shortname} بسبب ؛ {e}")


async def saves():
    try:
        os.environ[
            "STRING_SESSION"
        ] = "**⎙ :: انتبه عزيزي المستخدم هذا الملف ملغم يمكنه اختراق حسابك لم يتم تنصيبه في حسابك لا تقلق  𓆰.**"
    except Exception as e:
        print(str(e))
    try:
        await sbb_b(JoinChannelRequest("@jmthon"))
    except BaseException:
        pass
    try:
        await sbb_b(JoinChannelRequest("@RR7PP"))
    except BaseException:
        pass
    try:
        await sbb_b(JoinChannelRequest("@viosso"))
    except BaseException:
        pass


async def verifyLoggerGroup():
    """
    Will verify the both loggers group
    """
    flag = False
    if BOTLOG:
        try:
            entity = await sbb_b.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        "- الصلاحيات غير كافيه لأرسال الرسالئل في مجموعه فار ااـ PRIVATE_GROUP_BOT_API_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "لا تمتلك صلاحيات اضافه اعضاء في مجموعة فار الـ PRIVATE_GROUP_BOT_API_ID."
                    )
        except ValueError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID لم يتم العثور عليه . يجب التاكد من ان الفار صحيح."
            )
        except TypeError:
            LOGS.error(
                "PRIVATE_GROUP_BOT_API_ID قيمه هذا الفار غير مدعومه. تأكد من انه صحيح."
            )
        except Exception as e:
            LOGS.error(
                "حدث خطأ عند محاولة التحقق من فار PRIVATE_GROUP_BOT_API_ID.\n" + str(e)
            )
    else:
        descript = "⪼ هذه هي مجموعه الحفظ الخاصه بك لا تحذفها ابدا  𓆰."
        photobt = await sbb_b.upload_file(file="razan/razan/Jmthonp.jpg")
        _, groupid = await create_supergroup(
            "كروب بوت جمثون", sbb_b, Config.TG_BOT_USERNAME, descript, photobt
        )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print(
            "المجموعه الخاصه لفار الـ PRIVATE_GROUP_BOT_API_ID تم حفظه بنجاح و اضافه الفار اليه."
        )
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await sbb_b.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(
                        " الصلاحيات غير كافيه لأرسال الرسالئل في مجموعه فار ااـ PM_LOGGER_GROUP_ID."
                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(
                        "لا تمتلك صلاحيات اضافه اعضاء في مجموعة فار الـ  PM_LOGGER_GROUP_ID."
                    )
        except ValueError:
            LOGS.error(
                "PM_LOGGER_GROUP_ID يم تم العثور على قيمه هذا الفار . تاكد من أنه صحيح ."
            )
        except TypeError:
            LOGS.error("PM_LOGGER_GROUP_ID قيمه هذا الفار خطا. تاكد من أنه صحيح.")
        except Exception as e:
            LOGS.error("حدث خطأ اثناء التعرف على فار PM_LOGGER_GROUP_ID.\n" + str(e))
    else:
        descript = "❃ لا تحذف او تغادر المجموعه وظيفتها حفظ رسائل التي تأتي على الخاص"
        photobt = await sbb_b.upload_file(file="razan/razan/Jmthonp.jpg")
        _, groupid = await create_supergroup(
            "مجموعة التخزين", sbb_b, Config.TG_BOT_USERNAME, descript, photobt
        )
        addgvar("PM_LOGGER_GROUP_ID", groupid)
        print("تم عمل الكروب التخزين بنجاح واضافة الفارات اليه.")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "sbb_b"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)
