from log import *
from database.funcs import *
from config import *

from telegram.ext import ConversationHandler

DELETE_PRODUCT_NAME, DELETE_PRODUCT_OPTIONS = range(4, 6)


async def delete_product(update, context):
    check = check_barista(update.message.from_user.username)
    if update.message.from_user.id in ADMIN_IDS or check:
        await update.message.reply_text(
            "Введите название товара, который хотите удалить"
        )

        logger.info("__Start of delete_product__")
        return DELETE_PRODUCT_NAME
    else:
        await update.message.reply_text("Вы не являетесь админом или сотрудником")
        logger.warning(
            "User %s, %s tried to delete product",
            update.message.from_user.username,
            update.message.from_user.id,
        )
        return ConversationHandler.END


async def delete_product_name(update, context):
    context.user_data["product_name"] = update.message.text
    await update.message.reply_text(
        "Введите опции товара через запятую\nНапример: S, M, L\nЕсли опций нет, то просто напишите: Нет"
    )

    logger.info(
        "User %s choose a name of deleting product: %s",
        update.message.from_user.username,
        update.message.text,
    )
    return DELETE_PRODUCT_OPTIONS


async def delete_product_options(update, context):
    product_name = context.user_data["product_name"]
    product_options = update.message.text.split(", ")

    for option in product_options:
        check = check_product(product_name, option)

        if check == []:
            if option.lower() == "нет":
                await update.message.reply_text(f"Товара {product_name} не существует")
            else:
                await update.message.reply_text(
                    f"Товара {product_name} {option} не существует"
                )

            logger.info("Product %s not found", product_name)
        elif check[1] == 0:
            delete_product_DB(product_name, [option])
            if option.lower() == "нет":
                await update.message.reply_text(f"Товар {product_name} успешно удалён")
            else:
                await update.message.reply_text(
                    f"Товар {product_name} {option} успешно удалён"
                )

            logger.info(
                "User %s successfully deleted product: %s %s",
                update.message.from_user.username,
                product_name,
                option,
            )
        else:
            if option.lower() == "нет":
                await update.message.reply_text(f"Товар {product_name} уже удалён")
            else:
                await update.message.reply_text(
                    f"Товар {product_name} {option} уже удалён"
                )

            logger.info("Product %s %s already deleted", product_name, option)

    logger.info("__End of delete_product__")
    return ConversationHandler.END
