from log import *
from database.funcs import *
from config import *

from telegram import Bot


async def done(update, context):
    check = check_barista(update.message.from_user.username)
    if check:
        text = update.message.text.split()
        if 2 <= len(text) <= 3:
            user_id = get_user_by_code(int(text[1]))

            if user_id != -1:
                close_order(int(text[1]))

                if check_drink_in_order(text[1]) and len(text) != 3:
                    add_points(user_id, 1)
                    await update.message.reply_text(
                        "Клинету начислен 1 балл за покупку напитка"
                    )
                    points = get_points(user_id)
                    async with Bot(TOKEN) as bot:
                        await bot.send_message(
                            chat_id=user_id,
                            text=f"Спасибо за заказ!\nВам начислен 1 балл за покупку напитка.\nТекущий баланс: {points}",
                        )

                elif len(text) == 3:
                    points = int(text[2])
                    if points > get_points(user_id):
                        await update.message.reply_text(
                            f"У клинета не хватает баллов. Его текущий баланс: {get_points(user_id)}"
                        )
                        return
                    else:
                        use_points(user_id, int(text[2]))
                        await update.message.reply_text(
                            f"У клинета списано {text[2]} баллов"
                        )
                        points = get_points(user_id)
                        async with Bot(TOKEN) as bot:
                            await bot.send_message(
                                chat_id=user_id,
                                text=f"Спасибо за заказ!\nВы списали {text[2]} баллов.\nТекущий баланс: {points}",
                            )

                else:
                    async with Bot(TOKEN) as bot:
                        await bot.send_message(
                            chat_id=user_id, text=f"Спасибо за заказ!"
                        )

                user_linked_by = user_linked(user_id)
                if user_linked_by > 0:
                    async with Bot(TOKEN) as bot:
                        add_points(user_linked_by, 2)
                        await bot.send_message(
                            chat_id=user_linked_by,
                            text=f"Пользователь воспользовался вашей ссылкой. Вам начислено 2 балла!\nТекущий баланс: {get_points(user_linked_by)}",
                        )

                        add_points(user_id, 3)
                        await bot.send_message(
                            chat_id=user_id,
                            text=f"Реферальная ссылка использована. Вам начислено 3 балла!\nТекущий баланс: {points + 3}",
                        )

                        unlink_user(user_id)

                        logger.info(
                            "Users %s, %s used referral link", user_id, user_linked_by
                        )

                logger.info(
                    "Barista %s closed order %s",
                    update.message.from_user.username,
                    user_id,
                )
                await update.message.reply_text("Заказ выполнен")
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
