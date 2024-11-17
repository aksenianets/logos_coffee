import sqlite3
import random
import datetime

PATHTODB = "handlers/logos.db"
# Not DB funcs

# DB funcs
def generate_code() -> int:
    today = datetime.date.today()

    while True:
        code = random.randint(1, 999)

        get_query = f"""
            SELECT id FROM orders
            WHERE active = 1 AND date = "{today}" AND code = {code}
        """

        res = sqlite3.connect(PATHTODB).execute(get_query)
        res = [x for x in res if None not in x]

        if code in (id,) in res:
            continue
        else:
            return code

def add_user(user_id:int, linked_by:str="") -> None:
    add_query = f"""
            INSERT INTO users (user_id, points, linked_by)
            VALUES ({user_id}, 0, "{linked_by}")
        """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(add_query)

def check_user(user_id: int) -> bool:
    get_query = """SELECT user_id FROM users"""

    res = sqlite3.connect(PATHTODB).execute(get_query)
    res = [x[0] for x in res if None not in x]
    
    return user_id in res

def create_order() -> None:
    today = datetime.date.today()
    code = generate_code()

    create_query = f"""
        INSERT INTO orders (id, date, active)
        VALUES ({code}, "{today}", 1)
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(create_query)
        
def close_order(order_id: int) -> None:
    close_query = f"""
        UPDATE orders
        SET (id, date, active) = (id, date, 0)
        WHERE id = {order_id}
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(close_query)
    