from handlers.log import *
from handlers.funcs import *

from telegram import Bot
from telegram.ext import ConversationHandler
from config import *

FORWARD_FEEDBACK = range(1)

async def feedback(update, context):
    await update.message.reply_text("Чем бы вы хотели поделиться?")
    return FORWARD_FEEDBACK

async def forward_feedback(update, context):
    from_chat = update.message.chat_id
    message = update.message.id 
    async with Bot(TOKEN) as bot:
        for admin in ADMIN_IDS:
            await bot.send_message(chat_id=admin, text="Новый отзыв!", disable_notification=True)
            await bot.copy_message(chat_id=admin, from_chat_id=from_chat, message_id=message, disable_notification=True)
        employees = get_employees()
        for employee in employees:
            await bot.send_message(chat_id=employee, text="Новый отзыв!", disable_notification=True)
            await bot.copy_message(chat_id=employee, from_chat_id=from_chat, message_id=message, disable_notification=True)
    
    await update.message.reply_text("Спасибо за отзыв!")

    logger.info(f"User sent feedback")
    return ConversationHandler.END