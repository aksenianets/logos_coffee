from imports import *
import config

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.TOKEN).build()

    # user commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("invite", invite))
    application.add_handler(CommandHandler("order", order))

    # admin commands
    application.add_handler(CommandHandler("add_employee", add_employee))
    application.add_handler(CommandHandler("delete_employee", delete_employee))
    
    application.run_polling()
