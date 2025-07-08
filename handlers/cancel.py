from log import *
from database.funcs import *

from telegram.ext import ConversationHandler


async def cancel(update, context):
    await update.message.reply_text("Действие отменено")

    logger.info("User %s canceled the conversation.", update.message.from_user.username)
    return ConversationHandler.END
