from log import *
from database.funcs import *
from config import *
from telegram import Bot


async def add_barista(update, context):
    if update.message.from_user.id in ADMIN_IDS:
        text = update.message.text.split()
        if len(text) == 3:
            user_id, username = text[1], text[2][1:]
            if check_barista(username):
                if check_fired_status(username):
                    change_fired_status(username)
                    await update.message.reply_text("Вы успешно добавили бариста")
                else:
                    await update.message.reply_text("Бариста уже был добавлен")
            else:
                add_barista_DB(user_id, username)
                await update.message.reply_text("Вы успешно добавили бариста")
        else:
            await update.message.reply_text(
                "Извините, я вас не понял\nЧтобы добавить бариста напишите:\n/add_barista @username"
            )
    else:
        await update.message.reply_text("Вы не являетесь админом")
