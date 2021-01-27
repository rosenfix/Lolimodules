from .. import loader, utils
from telethon.tl.types import PeerChat as e
from telethon.tl.types import PeerUser as r
def register(cb):
    cb(SpamAllChMod())
class SpamAllChMod(loader.Module):
    strings = {'name': 'Spamall'}
    async def client_ready(self, client, db):
        self.db = db
        if self.db.get("SpamAllCh", "logging", {}) == None:
            self.db.set("SpamAllCh", "logging", True)
    async def spmcmd(self, event):
        args = utils.get_args_raw(event)
        reply = await event.get_reply_message()
        caption = False
        media = False
        if reply and not args:
            media = reply
        if not args and not reply:
            return await event.edit("<b>нет аргументов.</b>")
        if args and reply:
            caption = args
            media = reply
        await event.edit("<b>работаю...</b>")
        haha = await event.client.get_dialogs()
        err = 0
        suc = 0
        error_ch = ""
        success_ch = ""
        for i in haha:
            try:
                chat = i.entity.megagroup
            except:
                None
            if i.name.startswith("friendly-"):
                None
            elif type(i.message.to_id) == r:
                None
            elif chat or type(i.message.to_id) == e:
                try:
                    if media and caption:
                        await event.client.send_file(i.id, media.media, caption=caption)
                    elif media and not caption:
                        await event.client.send_file(i.id, media.media)
                    else:
                        await event.client.send_message(i.id, args)
                    suc += 1
                    success_ch += f"\n{suc})<code>{i.name}</code>"
                except:
                    err += 1
                    error_ch += f"\n{err})<code>{i.name}</code>"
        logg = self.db.get("SpamAllCh", "logging", {})
        if logg:
            return await event.respond(f"Отправленно в <b>{suc}</b> чат(ов):{success_ch}\nНе удалось отправить в <b>{err}</b> чат(ов):{error_ch}")
        else:
            return await event.respond(f"Отправленно в <b>{suc}</b> чат(ов)\nНе удалось отправить в <b>{err}</b> чат(ов)")
    async def spmlogcmd(self, event):
        logg = self.db.get("SpamAllCh", "logging", {})
        if logg == None or logg == False:
            self.db.set("SpamAllCh", "logging", True)
            await event.edit("Лог чатов изменен на <code>True</code>")
            return
        else:
            self.db.set("SpamAllCh", "logging", False)
            await event.edit("Лог чатов изменен на <code>False</code>")
            return
