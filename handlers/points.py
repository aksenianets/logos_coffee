from log import *
from database.funcs import *
from config import *


async def points(update, context):
    user_id = update.message.from_user.id
    points = get_points(user_id)
    await update.message.reply_text(
        f"Ваши баллы: {points}\nКаждые 5 баллов = бесплатный напиток!\n"
        + "Если вы хотите обменять баллы, сообщите об этом бариста"
    )
