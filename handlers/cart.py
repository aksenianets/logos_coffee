from handlers.log import *
from handlers.funcs import *

from telegram.ext import ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

CART_CHANGE = range(1)


async def cart(update, context):
    if context.user_data.get("cart"):
        text = "*Ваша корзина:*\n"
        total = 0
        print(context.user_data["cart"])
        for x in context.user_data["cart"]:
            x = x.split(", ")
            total += int(x[2])
            text += f"    {x[0]} {x[1]} \- {x[2]} руб\.\n"
        text += f"\n*Итого: {str(total)} руб\.*"
        func = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Заказать", callback_data="заказать")],
                [[InlineKeyboardButton("Удалить товар", callback_data="удалить")]],
            ]
        )
        await update.message.reply_text(text, reply_markup=func)
        return CART_CHANGE
    else:
        await update.message.reply_text("Ваша корзина пуста")
        return ConversationHandler.END


async def cart_change(update, context):
    pass
