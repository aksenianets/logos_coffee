from log import *
from database.funcs import *
from config import *

from telegram import Bot
from telegram.ext import ConversationHandler
from telegram import Bot

FORWARD_FEEDBACK = range(1)


async def feedback(update, context):
    await update.message.reply_text("Чем бы вы хотели поделиться?")
    return FORWARD_FEEDBACK


async def forward_feedback(update, context):
    from_chat = update.message.chat_id
    message = update.message.id
    async with Bot(TOKEN) as bot:
        for admin in ADMIN_IDS:
            await bot.send_message(
                chat_id=admin, text="Новый отзыв!", disable_notification=True
            )
            await bot.copy_message(
                chat_id=admin,
                from_chat_id=from_chat,
                message_id=message,
                disable_notification=True,
            )
        baristas = get_baristas()
        for barista in baristas:
            await bot.send_message(
                chat_id=barista, text="Новый отзыв!", disable_notification=True
            )
            await bot.copy_message(
                chat_id=barista,
                from_chat_id=from_chat,
                message_id=message,
                disable_notification=True,
            )

    await update.message.reply_text("Спасибо за отзыв!")

    logger.info(f"User sent feedback")
    return ConversationHandler.END
