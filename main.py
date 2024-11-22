from imports import *
import config

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters 
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
    
    application.run_polling()
