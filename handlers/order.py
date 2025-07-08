from log import *
from database.funcs import *
from config import *

from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

(
    ORDER_PRODUCT_TYPE,
    ORDER_PRODUCT_NAME,
    ORDER_PRODUCT_OPTION,
    ORDER_PRODUCT,
    CART_CHANGE,
    CART_DELETE,
) = range(6)


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
    check = check_user(update.message.from_user.id)
    # curr_hour = datetime.datetime.now().time().hour
    types = get_types()
    cart = [InlineKeyboardButton("Корзина", callback_data="cart")]

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
        reply_list.append(cart)
        types_page = InlineKeyboardMarkup(reply_list)
        context.user_data["types_page"] = reply_list

        await update.message.reply_text(
            "Выберите какого типа продукт Вы хотите заказать:", reply_markup=types_page
        )

        return ORDER_PRODUCT_NAME


async def order_product_name(update, context):
    query = update.callback_query
    await query.answer()
    products = get_products(query.data)

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

    if query.data == "cart":
        if context.user_data.get("cart"):
            text = "*Ваша корзина:*\n" + "\n"
            total = 0
            for x in context.user_data["cart"]:
                x = x.split(", ")
                total += int(x[2])
                text += f"    {x[0]} {x[1]} \- {x[2]} руб\.\n"
            text += f"\n*Итого: {str(total)} руб\.*"
            cart_keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Заказать", callback_data="order")],
                    [InlineKeyboardButton("Удалить товар", callback_data="delete")],
                    [InlineKeyboardButton("Назад", callback_data="back")],
                ]
            )
            await query.edit_message_text(
                text, reply_markup=cart_keyboard, parse_mode="MarkdownV2"
            )
            return CART_CHANGE
        else:
            await query.edit_message_text(
                "Ваша корзина пуста",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Назад", callback_data="back")]]
                ),
            )
            return ORDER_PRODUCT_OPTION
    else:
        await query.edit_message_text(
            "Выберите товар:", reply_markup=menu_keyboard(context.user_data["lens"])
        )
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

        await query.edit_message_text(
            "Выберите товар:", reply_markup=menu_keyboard(context.user_data["lens"])
        )

        return ORDER_PRODUCT_OPTION

    elif query.data == "next_page":
        from_to = context.user_data["lens"]
        if from_to[1] + from_to[2] < len(from_to[0]):
            from_to[1] += from_to[2]
        context.user_data["lens"] = from_to

        await query.edit_message_text(
            "Выберите товар:", reply_markup=menu_keyboard(context.user_data["lens"])
        )

        return ORDER_PRODUCT_OPTION

    options = get_options(query.data)

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
        await query.edit_message_text(
            f"Товар {query.data} добавлен в корзину\nХотите что-то ещё?",
            reply_markup=InlineKeyboardMarkup(context.user_data["types_page"]),
        )
        if context.user_data.get("cart"):
            context.user_data["cart"].append(query.data)
        else:
            context.user_data["cart"] = [query.data]
        return


async def order_product(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "back":
        await query.edit_message_text(
            "Выберите товар:", reply_markup=menu_keyboard(context.user_data["lens"])
        )
        return ORDER_PRODUCT_OPTION

    if context.user_data.get("cart"):
        context.user_data["cart"].append(query.data)
    else:
        context.user_data["cart"] = [query.data]

    name, option, price = query.data.split(", ")
    await query.edit_message_text(
        f"Товар {name} {option} добавлен в корзину\nХотите что-то ещё?",
        reply_markup=InlineKeyboardMarkup(context.user_data["types_page"]),
    )

    return ORDER_PRODUCT_NAME


async def cart_change(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "back":
        await query.edit_message_text(
            "Выберите какого типа продукт Вы хотите заказать:",
            reply_markup=InlineKeyboardMarkup(context.user_data["types_page"]),
        )
        return ORDER_PRODUCT_NAME

    elif query.data == "order":
        user_id = query.from_user.id
        code = generate_code()
        await query.edit_message_text(
            f"Ваш номер заказа: {code}\nКогда он будет готов. вам придёт уведомление",
        )

        async with Bot(TOKEN) as bot:
            for baristas in get_baristas():
                text, total = "\n", 0
                for x in context.user_data["cart"]:
                    x = x.split(", ")
                    total += int(x[2])
                    text += f"    {x[0]} {x[1]} \- {x[2]} руб\.\n"
                text += f"\n*Итого: {str(total)} руб\.*"

                await bot.send_message(
                    chat_id=baristas[1],
                    text=f"*Новый заказ\! Номер\: {code}*\n" + text,
                    parse_mode="MarkdownV2",
                )

        cart_names = [x.split(", ")[0] for x in context.user_data["cart"]]
        is_drink_in_cart = check_drink_in_cart(cart_names)
        create_order(user_id, code, is_drink_in_cart)

        return ConversationHandler.END

    elif query.data == "delete":
        btns, count = [], 0
        for x in context.user_data["cart"]:
            x = x.split(", ")
            btns.append([InlineKeyboardButton(f"{x[0]} {x[1]}", callback_data=count)])
            count += 1
        btns.append([InlineKeyboardButton("Назад", callback_data="back")])
        delete_keyboard = InlineKeyboardMarkup(btns)
        await query.edit_message_text(
            "Выберете товар, который вы хотите удалить:", reply_markup=delete_keyboard
        )

        return CART_DELETE


async def cart_delete(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "back":
        await query.edit_message_text(
            "Выберите какого типа продукт, Вы хотите заказать:",
            reply_markup=InlineKeyboardMarkup(context.user_data["types_page"]),
        )

        return ORDER_PRODUCT_NAME
    else:
        del context.user_data["cart"][int(query.data)]
        if context.user_data.get("cart"):
            text = "*Ваша корзина:*\n" + "\n"
            total = 0
            for x in context.user_data["cart"]:
                x = x.split(", ")
                total += int(x[2])
                text += f"    {x[0]} {x[1]} \- {x[2]} руб\.\n"
            text += f"\n*Итого: {str(total)} руб\.*"
            cart_keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Заказать", callback_data="order")],
                    [InlineKeyboardButton("Удалить товар", callback_data="delete")],
                    [InlineKeyboardButton("Назад", callback_data="back")],
                ]
            )
            await query.edit_message_text(
                text, reply_markup=cart_keyboard, parse_mode="MarkdownV2"
            )

            return CART_CHANGE
        else:
            await query.edit_message_text(
                "Ваша корзина пуста",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Назад", callback_data="back")]]
                ),
            )

            return ORDER_PRODUCT_OPTION
