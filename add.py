from asyncio import sleep

import random

from telethon import functions
from userbot.events import register


@register(outgoing=True, pattern="^.add (.*)")
async def add(event):
    numb = int(event.pattern_match.group(1))
    users = await event.client.get_participants(numb)
    reply = await event.get_reply_message()
    await event.edit(reply)
    for user in users:

        await sleep(0.1)

        try:
            await event.client(functions.messages.AddChatUserRequest(chat_id=reply, user_id=user.id, fwd_limit=10))
        except:
            await sleep(0.1)


@register(outgoing=True, pattern="^.addc (.*)")
async def add(event):
    numb = int(event.pattern_match.group(1))
    users = await event.client.get_participants(numb)
    reply = await event.get_reply_message()
    await event.edit(str(reply.message))
    for user in users:

        await sleep(0)

        try:
            await event.client(
                functions.channels.InviteToChannelRequest(
                    channel=str(reply.message), users=[user.id]))
        except:
            await sleep(0)