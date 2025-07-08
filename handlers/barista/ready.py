from log import *
from database.funcs import *
from config import *

from telegram import Bot


async def ready(update, context):
    check = check_barista(update.message.from_user.username)
    if check:
        text = update.message.text.split()
        if len(text) == 2:
            user_id = get_user_by_code(int(text[1]))

            if user_id != -1:
                async with Bot(TOKEN) as bot:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"Ваш заказ готов!\nНомер заказа: {text[1]}",
                    )
                await update.message.reply_text(
                    "Сообщение о готовности отправлено!\nПосле оплаты заказа напишите:\n/done <номер заказа>\n"
                    + "Если клиент хочет списать баллы, напишите:\n/done <номер заказа> <количество баллов>"
                )

                logger.info(
                    "Barista %s sent message about ready order to user %s",
                    update.message.from_user.username,
                    user_id,
                )
            else:
                await update.message.reply_text("Такого заказа нет")
        else:
            await update.message.reply_text(
                "Извините, я вас не понял. Чтобы выполнить заказ, напишите: /ready <номер заказа>"
            )
    else:
        await update.message.reply_text("Вы не являетесь бариста")
        logger.warning(
            f"User %s, %s tried to use /ready",
            update.message.chat.username,
            update.message.chat.id,
        )
