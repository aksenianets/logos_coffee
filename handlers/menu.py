from config import *
from handlers.log import *
from handlers.funcs import *

async def menu(update, context):
    check = check_barista(update.message.from_user.username)
    menu = get_menu()
    types = get_types()
    text = "*Меню:*\n"

    for i in types:
        on = f"    _{i}:_\n"
        for j in menu:
            if i == j[0] and j[2] != "нет" and j[4] == 1:
                on += f"         {j[1]} {j[2]} \- {j[3]}р\.\n"
            elif i == j[0] and j[4] == 1:
                on += f"         {j[1]} \- {j[3]}р\.\n"
        if len(on.split()) != 1:
            text += on

    if check or update.message.chat.id in ADMIN_IDS:
        text += f"\n*Стоп\-лист:*\n"
        for i in types:
            stop = f"    _{i}:_\n"
            for j in menu:
                if i == j[0] and j[2] != "нет" and j[4] == 0:
                    stop += f"         {j[1]} {j[2]} \- {j[3]}р\.\n"
                elif i == j[0] and j[4] == 0:
                    stop += f"         {j[1]} \- {j[3]}р\.\n"
            if len(stop.split()) != 1:
                text += stop
            
    logger.info("User %s opened menu", update.message.from_user.username)
    await update.message.reply_markdown_v2(text)

