from log import *
from database.funcs import *
from config import *

from telegram.ext import ConversationHandler

AVAILABILITY_PRODUCT_NAME, AVAILABILITY_PRODUCT_OPTIONS = range(6, 8)


async def change_product_availability(update, context):
    check = check_barista(update.message.from_user.username)
    if update.message.from_user.id in ADMIN_IDS or check:
        await update.message.reply_text(
            "Введите название товара, который хотите изменить"
        )

        logger.info("__Start of change_product_availability__")
        return AVAILABILITY_PRODUCT_NAME
    else:
        await update.message.reply_text("Вы не являетесь админом или сотрудником")

        logger.warning(
            "User %s, %s tried to change product availability",
            update.message.from_user.username,
            update.message.from_user.id,
        )
        return ConversationHandler.END


async def change_product_availability_name(update, context):
    context.user_data["product_name"] = update.message.text
    await update.message.reply_text(
        "Введите опции товара через запятую\nНапример: S, M, L\nЕсли опций нет, то просто напишите: Нет"
    )

    logger.info(
        "User %s choose a name of changing product availability: %s",
        update.message.from_user.username,
        update.message.text,
    )
    return AVAILABILITY_PRODUCT_OPTIONS


async def change_product_availability_options(update, context):
    product_name = context.user_data["product_name"]
    product_options = update.message.text.split(", ")

    if product_options[0].lower() == "нет":
        product_options = ["нет"]

    for option in product_options:
        check = check_availability(product_name, option)

        if check == 0:
            change_availability_DB(product_name, option)
            if option == "нет":
                await update.message.reply_text(f"Товар {product_name} теперь доступен")
            else:
                await update.message.reply_text(
                    f"Товар {product_name} {option} теперь доступен"
                )

            logger.info(
                "User %s successfully changed product availability: %s %s to 1",
                update.message.from_user.username,
                product_name,
                option,
            )
        elif check == 1:
            change_availability_DB(product_name, option)
            if option == "нет":
                await update.message.reply_text(
                    f"Товар {product_name} теперь недоступен"
                )
            else:
                await update.message.reply_text(
                    f"Товар {product_name} {option} теперь недоступен"
                )

            logger.info(
                "User %s successfully changed product availability: %s %s to 0",
                update.message.from_user.username,
                product_name,
                option,
            )
        else:
            await update.message.reply_text(
                f"Товара {product_name} {option} не существует"
            )

            logger.info("Product %s %s not found", product_name, option)

    logger.info("__End of change_product_availability__")
    return ConversationHandler.END
