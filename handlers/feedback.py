from handlers.log import *
from handlers.funcs import *

from telegram import Bot
from config import *

async def feedback(update, context):
    await update.message.reply_text("Чем бы вы хотели поделиться?")
    
    return "feedback"

async def forward_feedback(update, context):
    from_chat = update.message.chat_id
    message = update.message.id 
    async with Bot(TOKEN) as bot:
        for admin in ADMIN_IDS:
            await bot.send_message(chat_id=admin, text="Новый отзыв!")
            await bot.copy_message(chat_id=admin, from_chat_id=from_chat, message_id=message)
    
    await update.message.reply_text("Спасибо за отзыв!")

    logger.info(f"User sent feedback")