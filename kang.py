# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# modified by rfoxxxy (rfoxxxyz studio dev.)
# @rfoxxxyofficial 

""" Userbot module for kanging stickers or making new ones. """

import io
import math
import urllib.request
from os import remove as DelFile

from PIL import Image
from telethon.tl.types import DocumentAttributeFilename, MessageMediaPhoto

from userbot import CMD_HELP, bot, BOTLOG, BOTLOG_CHATID
from userbot.events import register
from asyncio import sleep

PACK_FULL = "Whoa! That's probably enough stickers for one pack, give it a break. \
A pack can't have more than 120 stickers at the moment."
PACK_FULL_RUS = "К сожалению, в одном наборе может быть не более 120 стикеров."


@register(outgoing=True, pattern="^.kang")
async def kang(args):
    """ For .kang command, kangs stickers or creates new ones. """
    user = await bot.get_me()
    if not user.username:
        user.username = user.first_name
    message = await args.get_reply_message()
    photo = None
    emojibypass = False
    is_anim = False
    emoji = ""
    await args.edit("`Preparing for kang.....`")
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            photo = io.BytesIO()
            photo = await bot.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split('/'):
            photo = io.BytesIO()
            await bot.download_file(message.media.document, photo)

        # For kanging other sticker
            if (DocumentAttributeFilename(file_name='sticker.webp') in
                    message.media.document.attributes):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        # For kanging Animated Stickers
        elif (DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in
              message.media.document.attributes):
            await bot.download_file(message.media.document, 'AnimatedSticker.tgs')
            #
            # !!! HACK HACK HACK HACK !!!
            # We have to check both as Telegram constantly moving
            # the attributes between 0 and 1
            #
            try:
                emoji = message.media.document.attributes[0].alt
            except AttributeError:
                emoji = message.media.document.attributes[1].alt
            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await args.edit("`Unsupported File!`")
            return
    else:
        await args.edit("`Reply to photo/sticker/document to kang it bruh`")
        return

    await args.edit("`Getting sticker type...`")

    if photo:
        splat = args.text.split()
        if not emojibypass:
            emoji = "🤔"
        pack = 1
        if len(splat) == 3:
            pack = splat[2]  # User sent both
            emoji = splat[1]
        elif len(splat) == 2:
            if splat[1].isnumeric():
                # User wants to push into different pack, but is okay with
                # thonk as emote.
                pack = int(splat[1])
            else:
                # User sent just custom emote, wants to push to default
                # pack
                emoji = splat[1]

        packname = f"a{user.id}_by_{user.username}_{pack}"
        packnick = f"@{user.username}'s pack {pack}"
        cmd = '/newpack'
        file = io.BytesIO()

        if not is_anim:
            image = await resize_photo(photo)
            file.name = "sticker.png"
            image.save(file, "PNG")
            await args.edit("`Kanging image sticker.....`")
        else:
            packname += "_anim"
            packnick += " animated"
            cmd = '/newanimated'
            await args.edit("`Kanging animated sticker.....`")

        response = urllib.request.urlopen(
            urllib.request.Request(f'http://t.me/addstickers/{packname}'))
        htmlstr = response.read().decode("utf8").split('\n')

        if "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>." not in htmlstr:
            async with bot.conversation('Stickers') as conv:
                await conv.send_message('/addsticker')
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packname)
                x = await conv.get_response()
                while x.text == PACK_FULL or x.text == PACK_FULL_RUS:
                    pack += 1
                    packname = f"a{user.id}_by_{user.username}_{pack}"
                    packnick = f"@{user.username}'s pack {pack}"
                    await args.edit("`Switching to Pack " + str(pack) +
                                    " due to insufficient space`")
                    await conv.send_message(packname)
                    x = await conv.get_response()
                    if x.text == "Invalid pack selected." or x.text == "Не выбран набор стикеров.":
                        await conv.send_message(cmd)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message(packnick)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        if is_anim:
                            await conv.send_file('AnimatedSticker.tgs', force_document=True)
                            DelFile('AnimatedSticker.tgs')
                        else:
                            file.seek(0)
                            await conv.send_file(file, force_document=True)
                        await conv.get_response()
                        await conv.send_message(emoji)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response()
                            await conv.send_message(f"<{packnick}>")
                        # Ensure user doesn't get spamming notifications
                        await conv.get_response()
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.send_message("/skip")
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        await conv.send_message(packname)
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        await conv.get_response()
                        # Ensure user doesn't get spamming notifications
                        await bot.send_read_acknowledge(conv.chat_id)
                        if BOTLOG:
                        	await args.client.send_message(
                                BOTLOG_CHATID,
            				    f"Different Sticker Pack created successfully. Your pack can be found [here](t.me/addstickers/{packname})")
                        await args.edit(
                            f"Sticker added in a Different Pack! This Pack is Newly created! Your pack can be found [here](t.me/addstickers/{packname}) \n" +
                            "**This message " +
        					"shall be self destructed in 5 seconds.**",
                            parse_mode='md')
                        await sleep(5)
                        await args.delete()
                        return
                if is_anim:
                    await conv.send_file('AnimatedSticker.tgs', force_document=True)
                    DelFile('AnimatedSticker.tgs')
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                await conv.get_response()
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message('/done')
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
        else:
            await args.edit("Userbot sticker pack \
doesn't exist! Making a new one!")
            async with bot.conversation('Stickers') as conv:
                await conv.send_message(cmd)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message(packnick)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                if is_anim:
                    await conv.send_file('AnimatedSticker.tgs', force_document=True)
                    DelFile('AnimatedSticker.tgs')
                else:
                    file.seek(0)
                    await conv.send_file(file, force_document=True)
                await conv.get_response()
                await conv.send_message(emoji)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response()
                    await conv.send_message(f"<{packnick}>")
                # Ensure user doesn't get spamming notifications
                await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.send_message("/skip")
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                await conv.send_message(packname)
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                await conv.get_response()
                # Ensure user doesn't get spamming notifications
                await bot.send_read_acknowledge(conv.chat_id)
                if BOTLOG:
                	await args.client.send_message(
            		    BOTLOG_CHATID,
            		    f"Sticker Pack created successfully. Your pack can be found [here](t.me/addstickers/{packname})")

        await args.edit(
            f"Sticker added! Your pack can be found [here](t.me/addstickers/{packname}) \n" +
            "**This message " +
        	"shall be self destructed in 5 seconds.**",
            parse_mode='md')
        await sleep(5)
        await args.delete()


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = (512, 512)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        image.thumbnail(maxsize)

    return image


CMD_HELP.update({
    "kang":
    ".kang\n"
    "Usage: Reply .kang to a sticker or an image to kang it to your userbot pack."
})

CMD_HELP.update({
    "kang":
    ".kang [emoji('s)]\n"
    "Usage: Works just like .kang but uses the emoji('s) you picked."
})

CMD_HELP.update({
    "kang":
    ".kang [number]\n"
    "Usage: Kang's the sticker/image to the specified pack but uses ðŸ¤” as emoji."
})

CMD_HELP.update({
    "kang":
    ".kang [emoji('s')] [number]\n"
    "Usage: Kang's the sticker/image to the specified pack and uses the emoji('s) you picked."
})

