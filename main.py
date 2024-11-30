from imports import *
import config

from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

if __name__ == "__main__":
    application = ApplicationBuilder().token(config.TOKEN).build()

    # user commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("invite", invite))
    application.add_handler(CommandHandler("menu", menu))
    
    feedback_handler = ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback), ],
        states={
            FORWARD_FEEDBACK: [MessageHandler(filters.TEXT & ~filters.COMMAND, forward_feedback)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)],
    )
    application.add_handler(feedback_handler)

    order_handler = ConversationHandler(
        entry_points=[CommandHandler("order", order_product_type)],
        states={
            ORDER_PRODUCT_NAME: [CallbackQueryHandler(order_product_name)],
            ORDER_PRODUCT_OPTION: [CallbackQueryHandler(order_product_option)],
            ORDER_PRODUCT: [CallbackQueryHandler(order_product)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)],
    )
    application.add_handler(order_handler)

    cart_handler = ConversationHandler(
        entry_points=[CommandHandler("cart", cart)],
        states={
            CART_CHANGE: [CallbackQueryHandler(cart_change)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)],
    )
    application.add_handler(cart_handler)

    # admin commands
    application.add_handler(CommandHandler("delete_barista", delete_barista))

    # employee commands
    application.add_handler(CommandHandler("change_status", change_status))
    application.add_handler(CommandHandler("become_barista", become_barista))

    add_product_handler = ConversationHandler(
        entry_points=[CommandHandler("add_product", add_product)],
        states={
            PRODUCT_TYPE: [CallbackQueryHandler(product_type_button), MessageHandler(filters.TEXT & ~filters.COMMAND, product_type)],
            PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_name)],
            PRODUCT_OPTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_options)],
            PRODUCT_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_price)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)],
    )
    application.add_handler(add_product_handler)

    delete_product_handler = ConversationHandler(
        entry_points=[CommandHandler("delete_product", delete_product)],
        states={
            DELETE_PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_product_name)],
            DELETE_PRODUCT_OPTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_product_options)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)],
    )
    application.add_handler(delete_product_handler)

    change_availability_handler = ConversationHandler(
        entry_points=[CommandHandler("change_availability", change_product_availability)],
        states={
            AVAILABILITY_PRODUCT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_product_availability_name)],
            AVAILABILITY_PRODUCT_OPTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_product_availability_options)]
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)],
    )
    application.add_handler(change_availability_handler)

    application.run_polling()
