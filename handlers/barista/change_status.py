from log import *
from database.funcs import *
from config import *


async def change_status(update, context):
    username = update.message.from_user.username
    if check_barista(username):
        change_barista_status(username)
        check_status = check_barista_status(username)

        if check_status:
            await update.message.reply_text("Статус сменён на рабочий")
        else:
            await update.message.reply_text("Статус сменён на нерабочий")

        logger.info(
            "Barista %s changed status to %s",
            update.message.from_user.username,
            check_status,
        )
    else:
        await update.message.reply_text("Вы не являетесь сотрудником")
        logger.warning(
            "User %s tried to change status", update.message.from_user.username
        )
