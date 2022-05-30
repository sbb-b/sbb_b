import asyncio
import math

import heroku3
import requests
import urllib3

from sbb_b import sbb_b

from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

Heroku = heroku3.from_key(Config.HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
HEROKU_API_KEY = Config.HEROKU_API_KEY


@sbb_b.ar_cmd(pattern="وضع (.*)")
async def variable(var):
    if Config.HEROKU_API_KEY is None:
        return await edit_delete(
            var,
            "عزيزي المستخدم يجب ان تعين معلومات الفارات التالية لاستخدام اوامر الفارات\n `HEROKU_API_KEY`\n `HEROKU_APP_NAME`.",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit_delete(
            var,
            "عزيزي المستخدم يجب ان تعين معلومات الفارات التالية لاستخدام اوامر الفارات\n `HEROKU_API_KEY`\n `HEROKU_APP_NAME`.",
        )
    rep = await var.get_reply_message()
    vra = None
    if rep:
        vra = rep.text
    if vra is None:
        return await edit_delete(
            var, "**⌔∮ يجب عليك الرد على النص او الرابط حسب الفار الذي تضيفه **"
        )
    exe = var.pattern_match.group(1)
    await edit_or_reply(var, "**⌔∮ جارِ وضع الفار انتظر قليلا**")
    heroku_var = app.config()
    if exe == "توقيت":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير الوقت الخاص بك\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير الوقت الخاص بك\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "رمز الاسم":
        variable = "TIME_JM"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار رمز الاسم\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار رمز الاسم \n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "المكرر":
        variable = "TKRAR"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار اسم امر مكرر\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار اسم مكرر \n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "البايو" or exe == "النبذة":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار البايو\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار البايو\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "الصورة" or exe == "الصوره":
        variable = "DIGITAL_PIC"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار الصورة\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار الصورة\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "زخرفة الارقام" or exe == "زخرفه الارقام":
        variable = "TI_FN"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار زخرفه الارقام\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار زخرفه الارقام\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "اسم" or exe == "الاسم":
        variable = "ALIVE_NAME"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار اسم المستخدم\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار اسم المستخدم\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "صورة الادمن" or exe == "صوره الادمن":
        variable = "ADJM_PIC"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار صورة الادمن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار صورة الادمن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "كروب التخزين":
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كروب التخزين\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كروب التخزين\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra
    if exe == "كروب الحفظ":
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1)
        if variable in heroku_var:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كروب الحفظ\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                var,
                "**⌔∮ تم بنجاح تغيير فار كروب الحفظ\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = vra


@sbb_b.ar_cmd(pattern="ازالة (.*)")
async def variable(event):
    if Config.HEROKU_API_KEY is None:
        return await edit_delete(
            event,
            "عزيزي المستخدم يجب ان تعين معلومات الفارات التالية لاستخدام اوامر الفارات\n `HEROKU_API_KEY`\n `HEROKU_APP_NAME`.",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit_delete(
            event,
            "عزيزي المستخدم يجب ان تعين معلومات الفارات التالية لاستخدام اوامر الفارات\n `HEROKU_API_KEY`\n `HEROKU_APP_NAME`.",
        )
    exe = event.text[5:]
    heroku_var = app.config()
    await edit_or_reply(event, "**⌔∮ جارِ حذف الفار انتظر قليلا**")
    if exe == "رمز الاسم":
        variable = "TIME_JM"
        await asyncio.sleep(1)
        if variable not in heroku_var:
            return await edit_or_reply(
                event, "**⌔∮ لم تتم اضافه فار رمز الاسم بالاصل.**"
            )
        await edit_or_reply(
            event,
            "**⌔∮ تم بنجاح حذف فار كروب الحفظ\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
        )
        del heroku_var[variable]
    if exe == "البايو" or exe == "النبذة":
        variable = "DEFAULT_BIO"
        await asyncio.sleep(1)
        if variable not in heroku_var:
            return await edit_or_reply(event, "**⌔∮ لم تتم اضافه فار البايو بالاصل.**")
        await edit_or_reply(
            event,
            "**⌔∮ تم بنجاح حذف فار البايو\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
        )
        del heroku_var[variable]
    if exe == "الصورة" or exe == "الصوره":
        variable = "DIGITAL_PIC"
        await asyncio.sleep(1)
        if variable not in heroku_var:
            return await edit_or_reply(event, "**⌔∮ لم تتم اضافه فار الصورة بالاصل.**")
        await edit_or_reply(
            event,
            "**⌔∮ تم بنجاح حذف فار الصورة\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
        )
        del heroku_var[variable]
    if exe == "صورة الادمن" or exe == "صوره الادمن":
        variable = "ADJM_PIC"
        await asyncio.sleep(1)
        if variable not in heroku_var:
            return await edit_or_reply(
                event, "**⌔∮ لم تتم اضافه فار صورة الادمن بالاصل.**"
            )
        await edit_or_reply(
            event,
            "**⌔∮ تم بنجاح حذف فار صورة الادمن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
        )
        del heroku_var[variable]
    if exe == "اسم" or exe == "الاسم":
        variable = "ALIVE_NAME"
        await asyncio.sleep(1)
        if variable not in heroku_var:
            return await edit_or_reply(event, "**⌔∮ لم تتم اضافه فار الاسم بالاصل.**")
        await edit_or_reply(
            event,
            "**⌔∮ تم بنجاح حذف فار الاسم\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
        )
        del heroku_var[variable]
    if exe == "زخرفة الارقام" or exe == "زخرفه الارقام":
        variable = "TI_FN"
        await asyncio.sleep(1)
        if variable not in heroku_var:
            return await edit_or_reply(
                event, "**⌔∮ لم تتم اضافه فار زخرفه الارقام بالاصل.**"
            )
        await edit_or_reply(
            event,
            "**⌔∮ تم بنجاح حذف فار زخرفه الارقام\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
        )
        del heroku_var[variable]
    if exe == "كروب التخزين":
        variable = "PM_LOGGER_GROUP_ID"
        await asyncio.sleep(1)
        if variable not in heroku_var:
            return await edit_or_reply(
                event, "**⌔∮ لم تتم اضافه فار كروب التخزين بالاصل.**"
            )
        await edit_or_reply(
            event,
            "**⌔∮ تم بنجاح حذف فار كروب التخزين\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
        )
        del heroku_var[variable]
    if exe == "كروب الحفظ":
        variable = "PRIVATE_GROUP_BOT_API_ID"
        await asyncio.sleep(1)
        if variable not in heroku_var:
            return await edit_or_reply(
                event, "**⌔∮ لم تتم اضافه فار كروب الحفظ بالاصل.**"
            )
        await edit_or_reply(
            event,
            "**⌔∮ تم بنجاح حذف فار كروب الحفظ\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
        )
        del heroku_var[variable]


@sbb_b.ar_cmd(pattern="وقت(?:\s|$)([\s\S]*)")
async def variable(event):
    if Config.HEROKU_API_KEY is None:
        return await edit_delete(
            event,
            "عزيزي المستخدم يجب ان تعين معلومات الفارات التالية لاستخدام اوامر الفارات\n `HEROKU_API_KEY`\n `HEROKU_APP_NAME`.",
        )
    if Config.HEROKU_APP_NAME is not None:
        app = Heroku.app(Config.HEROKU_APP_NAME)
    else:
        return await edit_delete(
            event,
            "عزيزي المستخدم يجب ان تعين معلومات الفارات التالية لاستخدام اوامر الفارات\n `HEROKU_API_KEY`\n `HEROKU_APP_NAME`.",
        )
    exe = event.text[5:]
    iraq = "Asia/Baghdad"
    cairo = "Africa/Cairo"
    jordan = "Asia/Amman"
    yman = "Asia/Aden"
    Syria = "Asia/Damascus"
    heroku_var = app.config()
    await edit_or_reply(event, "⌔∮ يتم جلب معلومات هذا الفار")
    if exe == "وقت العراق" or exe == "وقت عراق":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى العراق\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى العراق\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = iraq
    if exe == "وقت السعودية" or exe == "وقت السعوديه":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى السعودية\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى السعودية\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = iraq
    if exe == "وقت مصر":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى مصر\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى مصر\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = cairo
    if exe == "وقت الاردن":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى الاردن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى الاردن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = jordan
    if exe == "وقت اليمن":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى اليمن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى اليمن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = yman
    if exe == "وقت سوريا":
        variable = "TZ"
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى اليمن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        else:
            await edit_or_reply(
                event,
                "**⌔∮ تم بنجاح تغيير الوقت الى اليمن\n\n❃ جار اعادة تشغيل السورس انتظر من 2-5 دقائق ليتشغل مره اخرى**",
            )
        heroku_var[variable] = Syria


@sbb_b.ar_cmd(pattern="استخدامي$")
async def dyno_usage(dyno):
    if (HEROKU_APP_NAME is None) or (HEROKU_API_KEY is None):
        return await edit_delete(
            dyno,
            "عزيزي المستخدم يجب ان تعين معلومات الفارات التالية لاستخدام اوامر الفارات\n `HEROKU_API_KEY`\n `HEROKU_APP_NAME`.",
        )
    dyno = await edit_or_reply(dyno, "**- يتم جلب المعلومات انتظر قليلا**")
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("**خطا: يوجد شي غير صحيح حدث**\n\n" f">.`{r.reason}`\n")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]

    # - Used -
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    # - Current -
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    return await dyno.edit(
        "**استخدام الدينو**:\n\n"
        f" -> `استخدام الدينو لتطبيق`  **{Config.HEROKU_APP_NAME}**:\n"
        f"     •  `{AppHours}`**ساعات**  `{AppMinutes}`**دقائق**  "
        f"**|**  [`{AppPercentage}`**%**]"
        "\n\n"
        " -> الساعات المتبقية لهذا الشهر :\n"
        f"     •  `{hours}`**ساعات**  `{minutes}`**دقائق**  "
        f"**|**  [`{percentage}`**%**]"
    )


@sbb_b.ar_cmd(pattern="لوك$")
async def _(dyno):
    if (HEROKU_APP_NAME is None) or (HEROKU_API_KEY is None):
        return await edit_delete(
            dyno,
            "عزيزي المستخدم يجب ان تعين معلومات الفارات التالية لاستخدام اوامر الفارات\n `HEROKU_API_KEY`\n `HEROKU_APP_NAME`.",
        )
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        app = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await dyno.reply(
            " يجب التذكر من ان قيمه الفارات التاليه ان تكون بشكل صحيح \nHEROKU_APP_NAME\n HEROKU_API_KEY"
        )
    data = app.get_log()
    await edit_or_reply(
        dyno, data, deflink=True, linktext="**اخر 100 سطر في لوك هيروكو: **"
    )


def prettyjson(obj, indent=2, maxlinelength=80):
    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)
