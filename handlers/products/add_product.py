from log import *
from database.funcs import *
from config import *

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler

PRODUCT_TYPE, PRODUCT_NAME, PRODUCT_PRICE, PRODUCT_OPTIONS = range(4)


async def add_product(update, context):
    check = check_barista(update.message.from_user.username)
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
