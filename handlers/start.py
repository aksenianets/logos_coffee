from handlers.log import *
from handlers.funcs import *

from telegram.ext import ConversationHandler

async def start(update, context):
    check = check_user(update.message.from_user.id)
    if not check:
        text = (
            "Привет, здесь ты можешь заказать себе кофе или другую вкусняшку!\n"
            + "Подписывайся на наши соц.сети:\n"
            + "https://t.me/logos_coffee \n"
            + "https://clck.ru/3EfFdn \n"
            # + "https://www.instagram.com/logos_coffee_?igsh=YXp0b2YzMHFlamMy&utm_source=qr \n"
            + "Чтобы сделать заказ, напиши /order"
        )
        linked_by = update.message.text.split()
        
        if len(linked_by) == 2 and linked_by[1].isalpha():
            await update.message.reply_text(
                "Реферальная ссылка принята!\nПосле первой покупки ты получишь 3 балла"
            )
            add_user(update.message.from_user.id, linked_by[1])
            logger.info(
                logger.info(
                    "New user %s linked by %s",
                    update.message.from_user.username,
                    linked_by[1],
                )
            )
        else:
            await update.message.reply_text(text, disable_web_page_preview=True)
            add_user(update.message.from_user.id)
            logger.info("New user - %s", update.message.from_user.username)
    else:
        text = ("Подписывайся на наши соц.сети:\n"
            + "https://t.me/logos_coffee \n"
            + "https://www.instagram.com/logos_coffee \n"
            + "Чтобы сделать заказ, напиши /order"
        )
        await update.message.reply_text(text, disable_web_page_preview=True)

async def cancel(update, context):
    await update.message.reply_text("Действие отменено")

    logger.info("User %s canceled the conversation.", update.message.from_user.username)
    return ConversationHandler.END