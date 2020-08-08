from .. import loader, utils

from asyncio import sleep

import telethon

import random

from userbot.events import register

@register(outgoing=True, pattern="^.kickall (.*)")
async def kickall(event):
    numb = str(event.pattern_match.group(1))
    for _ in range(numb):
	    user = random.choice([i for i in await event.client.get_participants(event.to_id)])

	    await sleep(1)

	    # Попытка кика...
	    try:
		    await event.client.kick_participant(event.chat_id, user.id)
		    await sleep(0.5)
	    except:
		    return
