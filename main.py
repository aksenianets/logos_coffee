from imports import *
import config

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("invite", invite))

    application.run_polling()
