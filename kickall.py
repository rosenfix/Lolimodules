from .. import loader, utils, security

from asyncio import sleep

import telethon

from telethon import events

import random

from telethon.tl.types import ChatAdminRights, ChatBannedRights, PeerUser, PeerChannel
from telethon.errors import BadRequestError
from telethon.tl.functions.channels import EditAdminRequest, EditBannedRequest
from telethon.tl.functions.messages import EditChatAdminRequest

from userbot.events import register

@register(outgoing=True, pattern="^.kickall (.*)")
async def kickall(event):
    numb = int(event.pattern_match.group(1))
    await event.delete()
    for _ in range(numb):
	    user = random.choice([i for i in await event.client.get_participants(event.to_id)])

	    await sleep(0.1)

	    # Попытка кика...
	    try:
		    await event.client(EditBannedRequest(event.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=True)))

		    
	    except:
		    await sleep(0.1)