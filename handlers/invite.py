# import handlers.log, handlers.funcs


async def invite(update, context):
    await update.message.reply_markdown_v2(
        f"Вот твоя реферальная [ссылка](t.me/logos_coffee_bot?start={update.message.from_user.username})\nПросто отправь её своему другу"
    )
