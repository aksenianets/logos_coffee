import sqlite3
import random
import datetime

PATHTODB = "handlers/logos.db"
# Not DB funcs

# DB funcs

# admin funcs
def add_employee_DB(username:str) -> bool:
    try:
        add_query = f"""
                INSERT INTO staff (username, is_working)
                VALUES ("{username}", 0)
            """

        with sqlite3.connect(PATHTODB) as con:
            con.executescript(add_query)

        return True
    except:
        return False

def delete_employee_DB(username:str) -> bool:
    try:
        delete_query = f"""
            DELETE FROM staff
            WHERE username = "{username}"
        """

        with sqlite3.connect(PATHTODB) as con:
            con.executescript(delete_query)

        return True
    except:
        return False

def check_employee(username: str) -> bool:
    get_query = "SELECT username FROM staff"

    res = sqlite3.connect(PATHTODB).execute(get_query)
    res = [x[0] for x in res if None not in x]

    return username in res


def change_employee_status(username: str) -> None:
    change_query = f"""
        UPDATE staff SET is_working = 1 - is_working 
        WHERE username = "{username}"
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(change_query)

def check_employee_status(username: str) -> bool:
    check_query = f"""
        SELECT is_working FROM staff
        WHERE username = "{username}"
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(check_query).fetchone()[0]
        
    return res

# users funcs
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

def add_points(user_id: int, points: int) -> None:
    add_query = f"""
        UPDATE users
        SET points = points + {points}
        WHERE user_id = {user_id}
    """
    
    with sqlite3.connect(PATHTODB) as con:
        con.executescript(add_query)

# order funcs
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

