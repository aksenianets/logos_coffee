from handlers.log import *
from handlers.funcs import *

async def order(update, context):
    check = check_user(update.message.from_user.id)

    if not check:
        await update.message.reply_text("Вы не зарегистрированы. Пожалуйста сначала напишите /start")
    else:
        curr_hour = datetime.datetime.now().time().hour
        if not (8 <= curr_hour <= 19):
            await update.message.reply_text("Извинте, мы принимаем заказы только с 8:00 до 20:00")