from handlers.log import *
from handlers.funcs import *
from config import *

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

PRODUCT_TYPE, PRODUCT_NAME, PRODUCT_PRICE, PRODUCT_OPTIONS = range(4)
DELETE_PRODUCT_NAME, DELETE_PRODUCT_OPTIONS = range(4, 6)
AVAILABILITY_PRODUCT_NAME, AVAILABILITY_PRODUCT_OPTIONS = range(6, 8)


# product adding
async def add_product(update, context):
    check = check_barista("@" + update.message.from_user.username)
    if update.message.from_user.id in ADMIN_IDS or check:
        reply_list = []
        for product_type in get_types():
            btn = InlineKeyboardButton(product_type, callback_data=product_type)
            reply_list.append([btn])
        product_types = InlineKeyboardMarkup(reply_list)

        await update.message.reply_text(
            "Для начала выберите категорию нового товара из списка или напишите новую в сообщении",
            reply_markup=product_types,
        )

        logger.info("__Start of add_product__")
        return PRODUCT_TYPE
    else:
        # добавить оповещение админа о попытке добавить товар
        await update.message.reply_text("Вы не являетесь админом или сотрудником")
        logger.warning(
            "User %s, %s tried to add new product",
            update.message.from_user.username,
            update.message.from_user.id,
        )

        return ConversationHandler.END


async def product_type_button(update, context):
    query = update.callback_query
    await query.answer()
    context.user_data["product_type"] = query.data

    await query.edit_message_text(text="Введите название товара")

    logger.info(
        "User %s choose a type of product: %s",
        update.callback_query.from_user.username,
        query.data,
    )
    return PRODUCT_NAME


async def product_type(update, context):
    context.user_data["product_type"] = update.message.text

    await update.message.reply_text("Введите название товара")

    logger.info(
        "User %s choose a type of product: %s",
        update.message.from_user.username,
        update.message.text,
    )
    return PRODUCT_NAME


async def product_name(update, context):
    context.user_data["product_name"] = update.message.text
    await update.message.reply_text(
        "Введите опции товра через запятую\nНапример: S, M, L\nЕсли опций нет, то просто напишите: Нет"
    )

    logger.info(
        "User %s choose a name of product: %s",
        update.message.from_user.username,
        update.message.text,
    )
    return PRODUCT_OPTIONS


async def product_options(update, context):
    if update.message.text.lower() == "нет":
        product_options = ["нет"]
    else:
        product_options = update.message.text.split(", ")
    context.user_data["product_options"] = product_options

    if len(product_options) == 1:
        await update.message.reply_text("Введите цену товара")
    else:
        await update.message.reply_text(
            "Введите цены товара в соответсивии с порядком его опций через запятую"
        )

    logger.info(
        "User %s choose option(-s) of product: %s",
        update.message.from_user.username,
        product_options,
    )
    return PRODUCT_PRICE


async def product_price(update, context):
    product_prices = update.message.text.split(", ")
    try:
        temp = [int(x) for x in product_prices]
    except:
        await update.message.reply_text("Цена должна быть числом")
        return PRODUCT_PRICE

    product_options = context.user_data["product_options"]

    if len(product_options) != len(product_prices):
        await update.message.reply_text(
            "Количество цен должно соответсвовать количеству опций\nВведите цены ещё раз"
        )
        return PRODUCT_PRICE

    product_type = context.user_data["product_type"]
    product_name = context.user_data["product_name"]
    text = (
        "Новый продукт успешно добавлен!"
        + f"\nКатегория: {product_type}"
        + f"\nНазвание: {product_name}"
        + f"\n{'Опция' if len(product_options) == 1 else 'Опции'}: {', '.join(product_options)}"
        + f"\n{'Цена' if len(product_prices) == 1 else 'Цены'}: {', '.join(product_prices)}"
    )

    add_product_DB(product_type, product_name, product_prices, product_options)
    await update.message.reply_text(text)

    logger.info(
        "User %s successfully added new product: %s",
        update.message.from_user.username,
        context.user_data["product_name"],
    )
    logger.info("__End of add_product__")
    return ConversationHandler.END


# product deleting
async def delete_product(update, context):
    check = check_barista("@" + update.message.from_user.username)
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


# product changing availability
async def change_product_availability(update, context):
    check = check_barista("@" + update.message.from_user.username)
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
