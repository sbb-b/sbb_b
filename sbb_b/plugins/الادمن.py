import asyncio

from telethon.errors import BadRequestError
from telethon.errors import ChatAdminRequiredError as no_admin
from telethon.errors import ImageProcessFailedError, PhotoCropSizeSmallError
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import (
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    ChatAdminRights,
    ChatBannedRights,
    InputChatPhotoEmpty,
    MessageMediaPhoto,
)
from telethon.utils import get_display_name

from sbb_b import sbb_b
from sbb_b.Config import Config

from ..core.logger import logging
from ..core.managers import edit_delete as eod
from ..core.managers import edit_or_reply as eor
from ..helpers import media_type
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, ban_rz, demote_rz, mute_rz, promote_rz

# =================== STRINGS ============
PP_TOO_SMOL = "**- الصورة صغيرة جدا**"
PP_ERROR = "**فشل اثناء معالجة الصورة**"
NO_ADMIN = "**- عذرا انا لست مشرف هنا**"
NO_PERM = "**- ليست لدي صلاحيات كافيه في هذه الدردشة**"
CHAT_PP_CHANGED = "**- تم تغيير صورة الدردشة**"
INVALID_MEDIA = "**- ابعاد الصورة غير صالحة**"

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

ADJM_PIC = Config.ADJM_PIC
if ADJM_PIC:
    prmt_rz = ADJM_PIC
else:
    prmt_rz = promote_rz

if ADJM_PIC:
    bn_rz = ADJM_PIC
else:
    bn_rz = ban_rz

if ADJM_PIC:
    dmt_rz = ADJM_PIC
else:
    dmt_rz = demote_rz

if ADJM_PIC:
    mt_rz = ADJM_PIC
else:
    mt_rz = mute_rz


LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

# ================================================
from telethon.tl.types import ChannelParticipantsAdmins as admin
from telethon.tl.types import ChannelParticipantsKicked as banned


@sbb_b.ar_cmd(pattern="الرابط$")
async def _(event):
    ko = await edit_or_reply(event, "**يتم جلب الرابط انتظر **")
    try:
        r = await event.client(
            ExportChatInviteRequest(event.chat_id),
        )
    except no_admin:
        return await edit_or_reply(ko, "عذرا انت لست مشرف في هذه الدردشة", time=10)
    await edit_or_reply(ko, f"- رابط الدردشة\n {r.link}")


@sbb_b.ar_cmd(
    pattern="تنزيل الكل$",
    groups_only=True,
    require_admin=True,
)
async def demotal(e):
    sr = await e.client.get_participants(e.chat.id, filter=admin)
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "????"
    for i in sr:
        try:
            await e.client(EditAdminRequest(e.chat_id, i.id, newrights, rank))
            rz += 1
        except BadRequestError:
            return await eod(e, NO_PERM)
    await eor(e, f"- تم تنزيل {rz} من المشرفين ✓")


@sbb_b.ar_cmd(
    pattern="المحظورين$",
    groups_only=True,
    require_admin=True,
)
async def getbaed(event):
    try:
        users = await event.client.get_participants(event.chat_id, filter=banned)
    except Exception as e:
        return await eor(event, f"خطأ - {str(e)}")
    if len(users) > 0:
        msg = (
            f"✓ **قائمة المستخدمين المحظورين هنا**\n العدد الكلي : __{len(users)}__\n\n"
        )
        for user in users:
            if not user.deleted:
                msg += f"🛡 __[{user.first_name}]({user.id})__\n"
            else:
                msg += "☠️ حسابات محذوفة\n"
        await eor(event, msg)
    else:
        await eod(event, "- لا يوجد مستخدمين محظورين هنا")


@sbb_b.ar_cmd(
    pattern="الصورة (وضع|حذف)$",
    groups_only=True,
    require_admin=True,
)
async def set_group_photo(event):
    type = (event.pattern_match.group(1)).strip()
    if type == "وضع":
        replymsg = await event.get_reply_message()
        photo = None
        if replymsg and replymsg.media:
            if isinstance(replymsg.media, MessageMediaPhoto):
                photo = await event.client.download_media(message=replymsg.photo)
            elif "image" in replymsg.media.document.mime_type.split("/"):
                photo = await event.client.download_file(replymsg.media.document)
            else:
                return await eod(event, INVALID_MEDIA)
        if photo:
            try:
                await event.client(
                    EditPhotoRequest(
                        event.chat_id, await event.client.upload_file(photo)
                    )
                )
                await bot.send_file(
                    event.chat_id,
                    help_rz,
                    caption=f"**❃ صورة المجموعه تم تغييرها بنجاح**\n❃ الدردشة: {gpic.chat.title}",
                )
            except PhotoCropSizeSmallError:
                return await eod(event, PP_TOO_SMOL)
            except ImageProcessFailedError:
                return await eod(event, PP_ERROR)
            except Exception as e:
                return await eod(event, f"**خطأ : **`{str(e)}`")
            process = "تم تحديثها"
    else:
        try:
            await event.client(EditPhotoRequest(event.chat_id, InputChatPhotoEmpty()))
        except Exception as e:
            return await eod(event, f"**خطأ : **`{e}`")
        process = "تم حذفها"
        await eod(event, "**⪼ صورة المجموعه تم حذفها بنجاح ✔️**")
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#صورة_المجموعه\n"
            f"صورة المجموعه {process} بنجاح ✓ "
            f"الدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
        )


@sbb_b.ar_cmd(
    pattern="رفع مشرف(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def promote(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(event, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    user, rank = await get_user_from_event(event)
    if not rank:
        rank = "admin"
    if not user:
        return
    sbb_bevent = await eor(event, "⌔∮ جارِ رفع المستخدم في الدردشة")
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, new_rights, rank))
    except BadRequestError:
        return await sbb_bevent.edit(NO_PERM)
    await event.client.send_file(
        event.chat_id,
        prmt_rz,
        caption=f"**₰ المستخدم: [{user.first_name}](tg://user?id={user.id})\nتم رفعه مشرف\nالمجموعه: {event.chat.title}\nاللقب: {rank}**",
    )
    await event.delete()
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#رفع_مشرف \
            \nالمستخدم: [{user.first_name}](tg://user?id={user.id})\
            \nالدردشة: {get_display_name(await event.get_chat())} (**{event.chat_id}**)",
        )


@sbb_b.ar_cmd(
    pattern="تنزيل مشرف(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def demote(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(event, NO_ADMIN)
        return
    user, _ = await get_user_from_event(event)
    if not user:
        return
    sbb_bevent = await eor(event, "⌔∮ جاري تنزيل المستخدم من رتبة الاشراف")
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    rank = "????"
    try:
        await event.client(EditAdminRequest(event.chat_id, user.id, newrights, rank))
    except BadRequestError:
        return await sbb_bevent.edit(NO_PERM)
    await sbb_bevent.delete()
    await event.client.send_file(
        event.chat_id,
        dmt_rz,
        caption=f"**المستخدم: [{user.first_name}](tg://{user.id})\nتم حذف رتبته\nالدردشة: {event.chat.title}**",
    )


@sbb_b.ar_cmd(
    pattern="حظر(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def _ban_person(event):
    user, reason = await get_user_from_event(event)
    if not user:
        return
    if user.id == event.client.uid:
        return await eod(event, "**❃ عذرا لا يمكنك حظر نفسك **")
    sbb_bevent = await eor(event, "**⌔∮ تم حظر هذا المستخدم بنجاح**")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await sbb_bevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await sbb_bevent.edit(
            "**⌔∮ ليست لدي صلاحيات كافية لكنه لا يزال محظور**"
        )
    await sbb_bevent.delete()
    if reason:
        await event.client.send_file(
            event.chat_id,
            bn_rz,
            caption=f"**₰ المستخدم :{_format.mentionuser(user.first_name ,user.id)}\nتم حظره بنجاح\nالسبب : {reason}**",
        )
    else:
        await event.client.send_file(
            event.chat_id,
            bn_rz,
            caption=f"**₰ المستخدم :{_format.mentionuser(user.first_name ,user.id)}\nتم حظره من المجموعه**",
        )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#حظر\
                \nالمستخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)\
                \nالسبب : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"#حظر\
                \nالمستخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )


@sbb_b.ar_cmd(
    pattern="الغاء حظر(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def nothanos(event):
    user, _ = await get_user_from_event(event)
    if not user:
        return
    sbb_bevent = await eor(event, "⌔∮ جار الغاء حظر المستخدم")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await sbb_bevent.edit(
            f"**₰ المستخدم :{_format.mentionuser(user.first_name ,user.id)}\nتم الغاء حظره بنجاح**"
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغاء_حظر\n"
                f"المستخدم: [{user.first_name}](tg://user?id={user.id})\n"
                f"الدردشة: {get_display_name(await event.get_chat())}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await sbb_bevent.edit("⌔∮ لقد حدث خطأ اثناء محاولة الغاء الحظر")
    except Exception as e:
        await sbb_bevent.edit(f"**خطأ :**\n`{e}`")


@sbb_b.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, event.chat_id):
        try:
            await event.delete()
        except Exception as e:
            LOGS.info(str(e))


@sbb_b.ar_cmd(pattern="كتم(?:\s|$)([\s\S]*)")
async def startgmute(event):
    if event.is_private:
        await event.edit("**⌔∮ ربما ستحدث بعض الاخطاء و المشاكل**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == sbb_b.uid:
            return await edit_or_reply(event, "**⌔∮ عذرا لا يمكنني كتم نفسي **")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "**⌔∮ لا يمكنني الحصول على معلومات من هذا المستخدم**"
        )
    if is_muted(userid, "gmute"):
        return await eor(
            event,
            "**⪼ المستخدم**: {_format.mentionuser(user.first_name ,user.id)}\n**تم كتمه بنجاح**",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خطأ**\n`{e}`")
    else:
        if reason:
            await sbb_b.send_file(
                event.chat_id,
                mt_rz,
                caption=f"**⪼ المستخدم:  {_format.mentionuser(user.first_name ,user.id)}\nتم كتمه بنجاح\nالسبب: {reason}**",
            )
            await event.delete()
        else:
            await sbb_b.send_file(
                event.chat_id,
                mt_rz,
                caption=f"**⪼ المستخدم: {_format.mentionuser(user.first_name ,user.id)}\nتم كتمه بنجاح**",
            )
            await event.delete()
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


@sbb_b.ar_cmd(pattern="الغاء كتم(?:\s|$)([\s\S]*)")
async def endgmute(event):
    if event.is_private:
        await event.edit("**⌔∮ قد تحدث بعض الاخطاء و المشاكل**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == sbb_b.uid:
            return await edit_or_reply(event, "⌔∮ عذرا لا يمكنني كتم نفسي اصلا")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "**⌔∮ لا يمكنني الحصول على معلومات من هذا المستخدم**"
        )
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**⪼ المستخدم:  {_format.mentionuser(user.first_name ,user.id)}\nغير مكتوم اصلا** ",
        )
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خطأ**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"**⪼ المستخدم:  {_format.mentionuser(user.first_name ,user.id)}\nتم الغاء كتمه بنجاح ✓\nالسبب :{reason}**",
            )
        else:
            await edit_or_reply(
                event,
                f"**⪼ المستخدم:  {_format.mentionuser(user.first_name ,user.id)}\nتم الغاء كتمه بنجاح ✓**",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغاء_كتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#الغاء_كتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


@sbb_b.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()


@sbb_b.ar_cmd(
    pattern="طرد(?:\s|$)([\s\S]*)",
    groups_only=True,
    require_admin=True,
)
async def endmute(event):
    user, reason = await get_user_from_event(event)
    if not user:
        return
    rozevent = await edit_or_reply(event, "**- جاري طرد المستخدم انتظر**")
    try:
        await event.client.kick_participant(event.chat_id, user.id)
    except Exception as e:
        return await rozevent.edit(NO_PERM + f"\n{e}")
    if reason:
        await rozevent.edit(
            f"**⌔∮ تم بنجاح طرد [{user.first_name}](tg://user?id={user.id})\nالسبب: {reason}**"
        )
    else:
        await rozevent.edit(
            f"**- تم بنجاح طرد [{user.first_name}](tg://user?id={user.id}) !**"
        )
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            "#طرد\n"
            f"المستخدم: [{user.first_name}](tg://user?id={user.id})\n"
            f"الدردشه: {get_display_name(await event.get_chat())}(**{event.chat_id}**)\n",
        )


@sbb_b.ar_cmd(pattern="تثبيت( بالاشعار|$)")
async def pin(event):
    to_pin = event.reply_to_msg_id
    if not to_pin:
        return await edit_delete(event, "**⌔∮ يجب الرد على الرسالة لتثبيتها**", 5)
    options = event.pattern_match.group(1)
    is_silent = bool(options)
    try:
        await event.client.pin_message(event.chat_id, to_pin, notify=is_silent)
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"**{e}**", 5)
    await edit_delete(event, "**⌔∮ تم تثبيت الرساله بنجاح**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#تثبيت\
                \n**تم بنجاح تثبيت الرسالة في الدردشه**\
                \nالدردشة: {get_display_name(await event.get_chat())}(**{event.chat_id}**)\
                \nالاشعار: {is_silent}",
        )


@sbb_b.ar_cmd(pattern="الغاء تثبيت( الكل|$)")
async def pin(event):
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "الكل":
        return await edit_delete(
            event,
            "**❃ يجب الرد على رسالة لإلغاء تثبيتها **",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "الكل":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event, "**❃ يجب الرد على رسالة لإلغاء تثبيتها **", 5
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"**{e}**", 5)
    await edit_delete(event, "**❃ تم بنجاح الغاء التثبيت**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"#الغاء_تثبيت\
                \n**تم بنجاح الغاء تثبيت الرسالة**\
                \nالدردشه: {get_display_name(await event.get_chat())}(**{event.chat_id}**)",
        )


@sbb_b.ar_cmd(
    pattern="الاحداث( -u)?(?: |$)(\d*)?",
    groups_only=True,
    require_admin=True,
)
async def _iundlt(event):
    rozevent = await edit_or_reply(event, "**⌔∮ يتم البحث عن الأحداث**")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"**الرسائل المحذوفة {lim} الأخيرة في هذه المجموعة هي‌‌:**"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n• **{msg.old.message}** **ارسلت بواسطه** {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n• **{_media_type}** **ارسلت بواسطه** {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(rozevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(rozevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\n**ارسلت بواسطه** {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\n**ارسلت بواسطه** {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )
