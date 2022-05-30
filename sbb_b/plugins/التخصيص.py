from urlextract import URLExtract

from sbb_b import sbb_b
from sbb_b.core.logger import logging

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from . import BOTLOG_CHATID

LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER

extractor = URLExtract()

oldvars = {
    "PM_PIC": "pmpermit_pic",
    "PM_TEXT": "pmpermit_txt",
    "PM_BLOCK": "pmblock",
}


@sbb_b.ar_cmd(pattern="اضف (.*)")
async def custom_sbb_(event):
    reply = await event.get_reply_message()
    text = None
    if reply:
        text = reply.text
    if text is None:
        return await edit_delete(
            event, "**⌔∮ يجب عليك الرد على النص او الرابط حسب الفار الذي تضيفه **"
        )
    input_str = event.pattern_match.group(1)
    if (
        input_str == "كليشة الحماية"
        or input_str == "كليشة الحمايه"
        or input_str == "كليشه الحماية"
        or input_str == "كليشه الحمايه"
    ):
        addgvar("pmpermit_txt", text)
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        addgvar("ALIVE_TEMPLATE", text)
    if input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        addgvar("pmblock", text)
    if input_str == "كليشة البوت" or input_str == "كليشه البوت":
        addgvar("START_TEXT", text)
    if input_str == "ايموجي الفحص":
        addgvar("ALIVE_EMOJI", text)
    if input_str == "نص الفحص":
        addgvar("ALIVE_TEXT", text)
    if input_str == "عدد التحذيرات":
        addgvar("MAX_FLOOD_IN_PMS", text)
    if (
        input_str == "صورة الحماية"
        or input_str == "صورة الحمايه"
        or input_str == "صوره الحماية"
        or input_str == "صوره الحمايه"
    ):
        urls = extractor.find_urls(reply.text)
        if not urls:
            return await edit_delete(
                event, "**⪼ يجب عليك الرد على رابط تلجراف اولا**", 5
            )
        text = " ".join(urls)
        addgvar("pmpermit_pic", text)
    if input_str == "صورة الفحص" or input_str == "صوره الفحص":
        urls = extractor.find_urls(reply.text)
        if not urls:
            return await edit_delete(
                event, "**⪼ يجب عليك الرد على رابط تلجراف اولا**", 5
            )
        text = " ".join(urls)
        addgvar("ALIVE_PIC", text)
    await edit_or_reply(event, f"**₰ تم بنجاح تحديث فار {input_str} بنجاح 𓆰،**")
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#وضع_فار\
                    \n**{input_str}** تم تحديثه بنجاح في قاعده البيانات كـ:",
        )


@sbb_b.ar_cmd(pattern="حذف (.*)")
async def custom_sbb_b(event):
    input_str = event.pattern_match.group(1)
    if (
        input_str == "كليشة الحماية"
        or input_str == "كليشة الحمايه"
        or input_str == "كليشه الحماية"
        or input_str == "كليشه الحمايه"
    ):
        if gvarstatus("pmpermit_txt") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("pmpermit_txt")
    if input_str == "كليشة الفحص" or input_str == "كليشه الفحص":
        if gvarstatus("ALIVE_TEMPLATE") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("ALIVE_TEMPLATE")
    if input_str == "كليشة الحظر" or input_str == "كليشه الحظر":
        if gvarstatus("pmblock") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("pmblock")
    if (
        input_str == "صورة الحماية"
        or input_str == "صورة الحمايه"
        or input_str == "صوره الحماية"
        or input_str == "صوره الحمايه"
    ):
        if gvarstatus("pmpermit_pic") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("pmpermit_pic")
    if input_str == "صورة الفحص" or input_str == "صوره الفحص":
        if gvarstatus("ALIVE_PIC") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("ALIVE_PIC")
    if input_str == "كليشة البوت" or input_str == "كليشه البوت":
        if gvarstatus("START_TEXT") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("START_TEXT")
    if input_str == "ايموجي الفحص":
        if gvarstatus("ALIVE_EMOJI") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("ALIVE_EMOJI")
    if input_str == "نص الفحص":
        if gvarstatus("ALIVE_TEXT") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("ALIVE_TEXT")
    if input_str == "عدد التحذيرات":
        if gvarstatus("MAX_FLOOD_IN_PMS") is None:
            return await edit_delete(
                event, "**⎙ :: عزيزي المستخدم انت لم تقوم باضافه هذا الفار اصلا**"
            )
        delgvar("MAX_FLOOD_IN_PMS")
    await edit_or_reply(
        event, f"₰ هذا الفار تم حذفه بنجاح وارجاع قيمته الى القيمه الاصلية ✅"
    )
    if BOTLOG_CHATID:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#حذف_فار\
                    \n**فار {input_str}** تم حذفه من قاعده البيانات",
        )
