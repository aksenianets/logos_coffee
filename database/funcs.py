import sqlite3
import random
import datetime
import random

PATHTODB = "database/logos.db"


# admin funcs
def add_barista_DB(id: int, username: str) -> bool:
    try:
        add_query = f"""
                INSERT INTO staff (id, username, is_working)
                VALUES ({id}, "{username}", 0)
            """

        with sqlite3.connect(PATHTODB) as con:
            con.executescript(add_query)

        return True
    except:
        return False


def delete_barista_DB(username: str) -> bool:
    try:
        delete_query = f"""
            UPDATE staff SET fired = 1 
            WHERE username = "{username}"
        """

        with sqlite3.connect(PATHTODB) as con:
            con.executescript(delete_query)

        return True

    except:
        return False


def check_fired_status(username: str) -> bool:
    check_query = f"""
        SELECT fired FROM staff
        WHERE username = '{username}'
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(check_query).fetchone()[0]

    return res


def change_fired_status(username: str) -> None:
    change_query = f"""
        UPDATE staff SET fired = 0
        WHERE username = '{username}'
    """

    with sqlite3.connect(PATHTODB) as con:
        con.execute(change_query)


def check_barista(username: str) -> bool:
    get_query = f"""
        SELECT * FROM staff
        WHERE username = '{username}'
    """

    res = sqlite3.connect(PATHTODB).execute(get_query)

    return bool([x for x in res])


def change_barista_status(username: str) -> None:
    change_query = f"""
        UPDATE staff SET is_working = 1 - is_working 
        WHERE username = "{username}"
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(change_query)


def check_barista_status(username: str) -> bool:
    check_query = f"""
        SELECT is_working FROM staff
        WHERE fired = 0 AND
        username = "{username}"
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(check_query).fetchone()

    return [x for x in res][0] if res else False


def get_baristas() -> list:
    get_query = """
        SELECT username, id FROM staff
        WHERE fired = 0 AND
        is_working = 1
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(get_query).fetchall()

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
    get_query = """
        SELECT DISTINCT type FROM menu
        WHERE deleted = 0 AND avaible = 1
        ORDER BY -type
    """
    res = sqlite3.connect(PATHTODB).execute(get_query).fetchall()
    res = [x[0] for x in res]

    return res


def get_products(type: str) -> list:
    menu_query = f"""
        SELECT name, price FROM menu 
        WHERE type = '{type}' AND 
        deleted = 0 AND avaible = 1 
        ORDER BY name
    """

    with sqlite3.connect(PATHTODB) as con:
        products = con.execute(menu_query).fetchall()

    return products


def get_options(name: str) -> list:
    options_query = f"""
        SELECT option, price FROM menu 
        WHERE name = '{name}' AND avaible = 1
        AND deleted = 0 ORDER BY price
    """

    with sqlite3.connect(PATHTODB) as con:
        options = con.execute(options_query).fetchall()

    return options


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


def add_product_DB(
    product_type: str, name: str, prices: list[str], options: list[str]
) -> None:
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
        lower(name) = lower("{name}") AND
        lower(option) = lower("{option}") AND
        deleted = 0
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(get_query).fetchone()

        if res:
            return int(res[0])
        else:
            return 3


def change_availability_DB(name: str, option: str) -> None:
    with sqlite3.connect(PATHTODB) as con:
        change_query = f"""
            UPDATE menu SET avaible = 1 - avaible
            WHERE lower(name) = lower("{name}") AND
            lower(option) = lower("{option}")
        """

        con.executescript(change_query)


# users funcs
def add_user(user_id: int, linked_by: int = 0) -> None:
    try:
        add_query = f"""
                INSERT INTO users (user_id, points, linked_by)
                VALUES ({user_id}, 0, {linked_by})
            """

        with sqlite3.connect(PATHTODB) as con:
            con.executescript(add_query)
    except:
        pass


def user_linked(user_id: int) -> int:
    get_query = f"""
        SELECT linked_by FROM users
        WHERE user_id = {user_id}
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(get_query).fetchone()[0]

    return res


def unlink_user(user_id: int) -> None:
    update_query = f"""
        UPDATE users SET linked_by = -1
        WHERE user_id = {user_id}
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(update_query)


def check_user(user_id: int) -> bool:
    get_query = """SELECT user_id FROM users"""

    res = sqlite3.connect(PATHTODB).execute(get_query).fetchall()
    res = [x[0] for x in res]

    return user_id in res


def get_points(user_id: int):
    get_query = f"""
        SELECT points FROM users WHERE
        user_id = {user_id}
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(get_query).fetchone()[0]

    return res


def add_points(user_id: int, points: int) -> None:
    add_query = f"""
        UPDATE users
        SET points = points + {points}
        WHERE user_id = {user_id}
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(add_query)


def use_points(user_id: int, points: int) -> None:
    use_query = f"""
        UPDATE users
        SET points = points - {points}
        WHERE user_id = {user_id}
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(use_query)


# order funcs
def create_order(user_id: int, code: int, drink: bool) -> None:
    today = datetime.date.today()

    create_query = f"""
        INSERT INTO orders (id, date, active, code, drink)
        VALUES ({user_id}, "{today}", 1, {code}, {drink})
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(create_query)


def close_order(order_code: int) -> None:
    close_query = f"""
        UPDATE orders SET active = 0
        WHERE code = {order_code}
    """

    with sqlite3.connect(PATHTODB) as con:
        con.executescript(close_query)


def check_drink_in_cart(cart_names: list[str]) -> bool:
    get_query = """
        SELECT DISTINCT name FROM menu
        WHERE avaible = 1 AND deleted = 0
        AND type = "Напиток"
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(get_query).fetchall()
        res = [x[0] for x in res]

    for name in cart_names:
        if name in res:
            return True
        else:
            continue

    return False


def check_drink_in_order(code: int) -> bool:
    check_query = f"""
        SELECT drink FROM orders
        WHERE code = {code}
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(check_query).fetchone()[0]

    return bool(res)


def get_user_by_code(code: int) -> int:
    get_query = f"""
        SELECT id FROM orders
        WHERE active = 1 AND
        code = {code}
    """

    with sqlite3.connect(PATHTODB) as con:
        res = con.execute(get_query).fetchone()

    return res[0] if res else -1


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
