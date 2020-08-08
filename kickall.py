from .. import loader

from asyncio import sleep

import random

from userbot.events import register

@register(outgoing=True, pattern="^.kickall")
async def kickall(event):

    for _ in range(10):
	    user = random.choice([i for i in await event.client.get_participants(event.to_id)])

	    await event.respond('<b>Кому-то сейчас не повезёт...</b>')
	    await sleep(1)

	    # Попытка кика...
	    try:
		    await event.client.kick_participant(event.chat_id, user.id)
		    await sleep(0.5)
	    except:
		    return
