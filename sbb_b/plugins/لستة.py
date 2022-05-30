from asyncio import sleep

from geopy.geocoders import Nominatim
from telethon.tl import types

from ..core.managers import edit_or_reply
from ..helpers import reply_id
from . import sbb_b, reply_id


@sbb_b.ar_cmd(pattern="موقع ([\s\S]*)")
async def gps(event):
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, "⪼ يتم العثور على الموقع المطلوب")
    geolocator = Nominatim(user_agent="sbb_b")
    geoloc = geolocator.geocode(input_str)
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await event.client.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),
            caption=f"**الموقع : **{input_str}",
            reply_to=reply_to_id,
        )
        await catevent.delete()
    else:
        await catevent.edit("⪼ لم أجد الموقع 𓆰")


@sbb_b.ar_cmd(pattern="مؤقتا (\d*) ([\s\S]*)")
async def _(event):
    sbb_b = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = sbb_b[1]
    ttl = int(sbb_b[0])
    await event.delete()
    await sleep(ttl)
    await event.respond(message)
