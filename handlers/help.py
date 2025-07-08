from config import *
from log import *
from database.funcs import *


async def help(update, context):
    text = """
Если Вы хотите ознакомится с меню, напишите /menu\n
Если Вы хотите сделать заказ, добавить товар в корзину, посмотреть корзину, удалить товар из корзины, напишите /order\n
Если Вы хотите оставить отзыв, напишите /feedback\n
Если Вы хотите посмотреть сколько у вас баллов, напишите /points\n
Если Вы хотите пригласить друга, напишите /invite\n
Если Вы хотите остановить работу функции, напишите /cancel\n
    """
    username = update.message.from_user.username
    if check_barista(username):
        text += """
*Для бариста\:*\n
    Если Вы хотите добавить новый продукт, напишите /add\_product\n
    Если Вы хотите удалить продукт, напишите /delete\_product\n
    Если Вы хотите изменить доступность товара, то есть добавить его в стоп\-лист или убрать из него, напишите /change\_availability\n
    Если Вы хотите изменить свой статус на рабочий или на нерабочий, напишите /change\_status\n
    Если Вы хотите оповестить клиента о готовности заказа напишите /ready\n
    Если Вы хотите завершить заказ, напишите /done\n
    """
    if update.message.from_user.id in ADMIN_IDS:
        text += """
*Для админов\:*\n
    Если Вы хотите добавить бариста:\n
        1\) Попросите нового сотрудника узнать свой ID, для этого он должен написать команду /get\_id\n
        2\) После этого напишите /add\_barista \<ID\> @username\n
    Если Вы хотите удалить \(уволить\) бариста, напишите /delete\_barista @username
"""
    await update.message.reply_text(text, parse_mode="MarkdownV2")
