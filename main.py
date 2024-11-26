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


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.TOKEN).build()

    # user commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("order", order))
    application.add_handler(CommandHandler("invite", invite))
    
    feedback_handler = ConversationHandler(
        entry_points=[CommandHandler("feedback", feedback), ],
        states={
            "feedback": [MessageHandler(filters.TEXT & ~filters.COMMAND, forward_feedback)],
        },
        fallbacks=[MessageHandler(filters.COMMAND, cancel)],
    )
    application.add_handler(feedback_handler)

    # admin commands
    application.add_handler(CommandHandler("add_employee", add_employee))
    application.add_handler(CommandHandler("delete_employee", delete_employee))

    # employee commands
    application.add_handler(CommandHandler("change_status", change_status))

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
