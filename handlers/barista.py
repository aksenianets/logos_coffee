from handlers.log import *
from handlers.funcs import *
from config import *
from telegram import Bot

async def change_status(update, context):
    username = update.message.from_user.username
    check = check_barista(username)
    if check:
        change_barista_status(username)
        check_status = check_barista_status(username)

        if check_status:
            await update.message.reply_text("Статус сменён на рабочий")
        else:
            await update.message.reply_text("Статус сменён на нерабочий")

        logger.info("Employee %s changed status to %s", update.message.from_user.username, check_status)
    else:
        await update.message.reply_text("Вы не являетесь сотрудником")
        logger.warning("User %s tried to change status", update.message.from_user.username)

async def become_barista(update, context):
    text = update.message.text.split()
    if len(text) == 2:
        password = text[1]
        if password == open("handlers/password.txt", "r").read():
            add_barista_DB(update.message.from_user.id, update.message.from_user.username)
            await update.message.reply_text("Вы успешно стали бариста")
        else:
            await update.message.reply_text("Неверный пароль")
    else:
        await update.message.reply_text("Извините, я вас не понял\nЧтобы стать бариста напишите:\n/become_employee <пароль>")
    password = regenerate_password()
    async with Bot(TOKEN) as bot:
        for admin in ADMIN_IDS:
            await bot.send_message(chat_id=admin, text=f"Добавлен новый бариста: @{update.message.from_user.username}\nНовый пароль: {password}")