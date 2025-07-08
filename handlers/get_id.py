from log import *
from database.funcs import *
from config import *


async def get_id(update, context):
    user_id = update.effective_user.id
    await update.message.reply_text(f"Ваш ID: `{user_id}`", parse_mode="MarkdownV2")
