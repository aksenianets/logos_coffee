from handlers.log import *

# from handlers.funcs import *


async def start(update, context):
    text = (
        "Привет, здесь ты можешь заказать себе кофе или другую вкусняшку!\n"
        + "Подписывайся на нас в соц.сетях:\n"
        + "https://t.me/logos_coffee \n"
        + "https://www.instagram.com/logos_coffee_?igsh=YXp0b2YzMHFlamMy&utm_source=qr \n"
        + "Чтобы сделать заказ, напиши /order"
    )

    # добавление в БД юзера
    linked_by = update.message.text.split()
    await update.message.reply_text(text)
    if len(linked_by) == 2 and linked_by[1].isalpha():
        await update.message.reply_text(
            "Реферальная ссылка принята!\nПосле первой покупки ты получишь 3 балла"
        )
        logger.info(
            logger.info(
                "new user %s linked by %s",
                update.message.from_user.username,
                linked_by[1],
            )
        )
    else:
        logger.info("new user - %s", update.message.from_user.username)
