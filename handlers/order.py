from handlers.log import *
from handlers.funcs import *

from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import sqlite3

PATHTODB = "handlers/logos.db"

ORDER_PRODUCT_TYPE, ORDER_PRODUCT_NAME, ORDER_PRODUCT_OPTION, ORDER_PRODUCT = range(4)

def menu_keyboard(from_to: list):
    start = from_to[1]
    end = min(start + from_to[2], len(from_to[0]))
    current_page_items = from_to[0][start:end]
    
    navigation = []
    if from_to[1] > 0:
        navigation.append(InlineKeyboardButton("<", callback_data="prev_page"))
    navigation.append(InlineKeyboardButton("Назад", callback_data="back"))
    if end < len(from_to[0]):
        navigation.append(InlineKeyboardButton(">", callback_data="next_page"))

    return InlineKeyboardMarkup(current_page_items + [navigation])

async def order_product_type(update, context):
    logger.info("__Start order_product_type__")

    check = check_user(update.message.from_user.id)
    curr_hour = datetime.datetime.now().time().hour
    types = get_types()

    if not check:
        await update.message.reply_text(
            "Вы не зарегистрированы. Пожалуйста сначала напишите /start"
        )
        return ConversationHandler.END
    # elif not (8 <= curr_hour <= 19):
    #     await update.message.reply_text("Извинте, мы принимаем заказы только с 8:00 до 20:00")
    #     return ConversationHandler.END
    else:
        reply_list = []
        for product_type in types:
            btn = InlineKeyboardButton(product_type, callback_data=product_type)
            reply_list.append([btn])
        types_page = InlineKeyboardMarkup(reply_list)
        context.user_data["types_page"] = reply_list  # кнопки типов

        await update.message.reply_text(
            "Выберите какого типа продукт Вы хотите заказать:", reply_markup=types_page
        )
        return ORDER_PRODUCT_NAME


async def order_product_name(update, context):
    query = update.callback_query
    await query.answer()

    menu_query = f"""SELECT name, price FROM menu WHERE type = '{query.data}' AND deleted = 0 ORDER BY name"""
    with sqlite3.connect(PATHTODB) as con:
        products = con.execute(menu_query).fetchall()

    product_prices = {}
    for name, price in products:
        if name not in product_prices:
            product_prices[name] = []
        product_prices[name].append(price)

    reply_list = []
    for name, prices in product_prices.items():
        if len(prices) == 1:
            product_name = f"{name} - {prices[0]} руб."
        else:
            product_name = f"{name} - от {min(prices)} до {max(prices)} руб."
        btn = InlineKeyboardButton(product_name, callback_data=name)
        reply_list.append([btn])

    context.user_data["lens"] = [reply_list, 0, 4]

    await query.edit_message_text("Выберите товар:", reply_markup=menu_keyboard(context.user_data["lens"]))
    return ORDER_PRODUCT_OPTION


async def order_product_option(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "back":
        await query.edit_message_text(
            "Выберите какого типа продукт Вы хотите заказать:",
            reply_markup=InlineKeyboardMarkup(context.user_data["types_page"]),
        )
        return ORDER_PRODUCT_NAME

    if query.data == "prev_page":
        from_to = context.user_data["lens"]
        if from_to[1] - from_to[2] >= 0:
            from_to[1] -= from_to[2]
        context.user_data["lens"] = from_to
    
        await query.edit_message_text("Выберите товар:", reply_markup=menu_keyboard(context.user_data["lens"]))

        return ORDER_PRODUCT_OPTION

    elif query.data == "next_page":
        from_to = context.user_data["lens"]
        if from_to[1] + from_to[2] < len(from_to[0]):
            from_to[1] += from_to[2]
        context.user_data["lens"] = from_to
    
        await query.edit_message_text("Выберите товар:", reply_markup=menu_keyboard(context.user_data["lens"]))

        return ORDER_PRODUCT_OPTION

    options_query = f"""SELECT option, price FROM menu WHERE name = '{query.data}' AND deleted = 0 ORDER BY price"""
    with sqlite3.connect(PATHTODB) as con:
        options = con.execute(options_query).fetchall()

    if options[0][0] != "нет":
        reply_list = []
        for opt, price in options:
            btn = InlineKeyboardButton(
                f"{opt} - {price} руб.", callback_data=f"{query.data}, {opt}, {price}"
            )
            reply_list.append([btn])
        reply_list.append([InlineKeyboardButton("Назад", callback_data="назад")])

        product_options = InlineKeyboardMarkup(reply_list)
        await query.edit_message_text(
            f"Выберите опцию для {query.data}:", reply_markup=product_options
        )
        return ORDER_PRODUCT
    else:
        btn = [InlineKeyboardButton("Заказать", callback_data="заказать")]
        await query.edit_message_text(
            f"Товар {query.data} добавлен в корзину\nХотите что-то ещё?",
            reply_markup=InlineKeyboardMarkup(context.user_data["types_page"] + [btn]),
        )
        if context.user_data.get("cart"):
            context.user_data["cart"].append(query.data)
        else:
            context.user_data["cart"] = [query.data]
        return ORDER_PRODUCT_TYPE


async def order_product(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "назад":
        await query.edit_message_text("Выберите товар:", reply_markup=menu_keyboard(context.user_data["lens"]))
        return ORDER_PRODUCT_OPTION

    btn = [InlineKeyboardButton("Заказать", callback_data="заказать")]
    if context.user_data.get("cart"):
        context.user_data["cart"].append(query.data)
    else:
        context.user_data["cart"] = [query.data]

    name, option, price = query.data.split(", ")
    await query.edit_message_text(
        f"Товар {name} {option} добавлен в корзину\nХотите что-то ещё?",
        reply_markup=InlineKeyboardMarkup(context.user_data["types_page"] + [btn]),
    )

    return ORDER_PRODUCT_NAME
