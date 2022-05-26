# @Jmthon - < https://t.me/Jmthon >
# Copyright (C) 2021 - JMTHON-AR
# All rights reserved.
#
# This file is a part of < https://github.com/JMTHON-AR/JMTHON >
# Please read the GNU Affero General Public License in;
# < https://github.com/JMTHON-AR/JM-THON/blob/master/LICENSE
# ===============================================================
import os
import sys

try:
    pass
except ModuleNotFoundError:
    os.system("pip3 install py-tgcalls")

from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from ..Config import Config
from .client import JmthonUserBotClient

__version__ = "2.10.6"

loop = None

if Config.STRING_SESSION:
    session = StringSession(str(Config.STRING_SESSION))
else:
    session = "jmthon"

try:
    jmthon = JmthonUserBotClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        loop=loop,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
except Exception as e:
    print(f"[STRING SESSION] - {str(e)}")
    sys.exit()

if Config.STRING_2:
    session2 = StringSession(str(STRING_2))
    JMTHON2 = JmthonUserBotClient(
        session=session2,
        api_id=API_KEY,
        api_hash=API_HASH,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
else:
    JMTHON2 = None

jmthon.tgbot = tgbot = JmthonUserBotClient(
    session="JmthonTgbot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    loop=loop,
    app_version=__version__,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
).start(bot_token=Config.TG_BOT_TOKEN)
