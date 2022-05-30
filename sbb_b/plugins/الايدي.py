from telethon.utils import pack_bot_file_id

from sbb_b import sbb_b
from sbb_b.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply

LOGS = logging.getLogger(__name__)


@sbb_b.ar_cmd(pattern="الايدي(?:\s|$)([\s\S]*)")
async def _(roze):
    input_str = roze.pattern_match.group(2)
    if input_str:
        try:
            p = await roze.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(roze, f"`{e}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    roze, f"⌔∮ الايدي الخاص بـ `{input_str}` هو\n⪼ `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        roze, f"⌔∮ الايدي الخاص بـ `{p.title}` هو\n⪼ `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(roze, "**⌔∮ يجب أن تضع معرف المستخدم أو ترد على المستخدم**")
    elif roze.reply_to_msg_id:
        r_msg = await roze.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                roze,
                f"**⪼: معرف الدردشة الحالي : **`{roze.chat_id}`\n**⪼ ايدي المستخدم: **`{r_msg.sender_id}`\n**⪼ ايدي الميديا: **`{bot_api_file_id}`",
            )

        else:
            await edit_or_reply(
                roze,
                f"**⌔∮ ايدي الدردشه الحاليه : **`{roze.chat_id}`\n**⪼ ايدي المستخدم: **`{r_msg.sender_id}`",
            )

    else:
        await edit_or_reply(roze, f"**⌔∮ ايدي الدردشه الحاليه : **`{roze.chat_id}`")
