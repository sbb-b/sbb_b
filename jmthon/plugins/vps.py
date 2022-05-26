import glob
import os

from jmthon import jmthon

from ..core.managers import edit_or_reply
from ..helpers.utils import _jmthonutils

# ============================@ Constants @===============================
exts = ["jpg", "png", "webp", "webm", "m4a", "mp4", "mp3", "tgs"]

cmds = [
    "rm -rf downloads",
    "mkdir downloads",
]
# ========================================================================


@jmthon.ar_cmd(pattern="(ري|رست)لود$")
async def _(event):
    cmd = event.pattern_match.group(1)
    jmthon = await edit_or_reply(event, "**⌔∮ انتظر من 2-3 دقائق**")
    if cmd == "رست":
        for file in exts:
            removing = glob.glob(f"./*.{file}")
            for i in removing:
                os.remove(i)
        for i in cmds:
            await _jmthonutils.runcmd(i)
    await event.client.reload(jmthon)
