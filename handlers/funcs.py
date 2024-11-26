import sqlite3
import random
import datetime

PATHTODB = "handlers/logos.db"

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
            UPDATE staff SET fired = 1 
            WHERE username = "{username}
        """

        with sqlite3.connect(PATHTODB) as con:
            con.executescript(delete_query)

        return True
    except:
        return False

def check_employee(username: str) -> bool:
    get_query = "SELECT username FROM staff WHERE fired = 0"

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
        WHERE fired = 0 AND
        username = "{username} "
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(check_query).fetchone()[0]
        
    return res

# menu funcs
def get_menu() -> list:
    get_query = f"""
        SELECT type, name, option, price, avaible
        FROM menu WHERE deleted = 0
    """

    with sqlite3.connect(PATHTODB) as con:
        res = sqlite3.connect(PATHTODB).execute(get_query)
        res = [x for x in res]
    
    return res

def get_types() -> list:
    get_query = "SELECT type FROM menu WHERE deleted = 0 AND avaible = 1"
    res = sqlite3.connect(PATHTODB).execute(get_query)
    res = [x[0] for x in res if None not in x]

    return [x for x in set(res)]

def check_product(name: str, option: str) -> list[str]:
    get_query = f"""
        SELECT name, deleted FROM menu WHERE
        name = "{name}" AND
        option = "{option}"
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(get_query).fetchone()
        if res:    
            res = [x for x in res]
        else:
            res = []

    return res

def add_product_DB(product_type: str, name: str, prices: list[str], options: list[str]) -> None:
    with sqlite3.connect(PATHTODB) as con:
        for price, option in zip(prices, options):
            if check_product(name, option) == []:
                add_query = f"""
                    INSERT INTO menu (type, name, price, option)
                    VALUES ("{product_type}", "{name}", {int(price)}, "{option}")
                """
            elif check_product(name, option)[1] == 1:
                add_query = f"""
                    UPDATE menu SET (price, option, deleted) = ({int(price)}, "{option}", 0)
                    WHERE name = "{name}" AND option = "{option}"
                """
            else:
                add_query = f"""
                    UPDATE menu SET (price, option) = ({int(price)}, "{option}")
                    WHERE name = "{name}" AND option = "{option}" 
                """

            con.executescript(add_query)

def delete_product_DB(name: str, options: list[str]) -> None:
    with sqlite3.connect(PATHTODB) as con:
        for option in options:
            delete_query = f"""
                UPDATE menu SET deleted = 1
                WHERE name = "{name}" AND
                option = "{option}"
            """

            con.executescript(delete_query)
    
def check_availability(name: str, option: str) -> int:
    get_query = f"""
        SELECT avaible FROM menu WHERE
        name = "{name}" AND
        option = "{option}" AND
        deleted = 0
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(get_query).fetchone()[0]
        if res:
            return res
        else:
            return 3


def change_availability_DB(name: str, option: str) -> None:
    with sqlite3.connect(PATHTODB) as con:
        change_query = f"""
            UPDATE menu SET avaible = 1 - avaible
            WHERE name = "{name}" AND
            option = "{option}"
        """

        con.executescript(change_query)


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

