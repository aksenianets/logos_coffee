from handlers.log import *
from handlers.funcs import *
from config import *

async def add_employee(update, context):
    if update.message.from_user.id in ADMIN_IDS:
        text = update.message.text.split()
        if len(text) == 2:
            if add_employee_DB(text[1]):
                await update.message.reply_text("Бариста успешно добавлен")
                logger.info(f"Barista {text[1]} successfully added")
            else:
                await update.message.reply_text("Бариста уже добавлен или произошла ошибка")
        else:
            await update.message.reply_text("После команды введите имя пользователя через пробел\nПример: /add_employee @employee1")
    else:
        await update.message.reply_text("Вы не являетесь админом")
        logger.warning(f"User {update.message.from_user.id}, {update.message.from_user.username} tried to add employee")

async def delete_employee(update, context):
    if update.message.from_user.id in ADMIN_IDS:
        text = update.message.text.split()
        if len(text) == 2:
            if delete_employee_DB(text[1]):
                await update.message.reply_text("Бариста успешно удалён")
                logger.info(f"Barista {text[1]} successfully deleted")
            else:
                await update.message.reply_text("Барисста уже удалён или произошла ошибка")
        else:
            await update.message.reply_text("После команды введите имя пользователя через пробел\nПример: /delete_employee @employee1")
    else:
        await update.message.reply_text("Вы не являетесь админом")
        logger.warning(f"User {update.message.from_user.id}, {update.message.from_user.username} tried to delete employee")

