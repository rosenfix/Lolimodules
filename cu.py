from telethon import functions, types
from .. import loader, utils
import io
import os
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.users import GetFullUserRequest
def register(cb):
    cb(CuMod())
class CuMod(loader.Module):
    """Полное копирование юзера(ава, имя фамилия, био)"""
    strings = {'name': 'Cu'}
    def __init__(self):
        self.name = self.strings['name']
        self._me = None
        self._ratelimit = []
    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self.me = await client.get_me()
    async def cucmd(self, message):
        'Скопировать юзера'
        reply = await message.get_reply_message().from_id))
        try:
            reply.sender
        except:
            await message.edit("ДАЙ МНЕ БЛЯТЬ РЕПЛАЙ НА ЮЗЕРА ТЫ ЕБАНАЯ ХУЙНЯ")
            return
        await message.edit("Качаем аву...")
        ava = await message.client.download_profile_photo(reply.sender)
        up = await message.client.upload_file(ava)
        await message.edit("Ставим аву...")
        avs = await message.client.get_profile_photos('me')
        if len(avs) > 0:
            await message.client(functions.photos.DeletePhotosRequest(await message.client.get_profile_photos('me')))
        await message.client(functions.photos.UploadProfilePhotoRequest(up))
        await message.edit("Пиздим имя и фамилию и био...")
        full = await message.client(GetFullUserRequest(reply.sender.id))
        fname = reply.sender.first_name
        if reply.sender.last_name == None:
            lname = ""
        else:
            lname = reply.sender.last_name
        if full.about == None:
            bio = ""
        else:
            bio = full.about
        await message.client(UpdateProfileRequest(
            fname,
            lname,
            bio
        ))
        await message.edit("Юзер клонирован")
        os.remove(ava)
        

