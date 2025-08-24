import time
import uuid
import sqlite3


def get_product(conn: sqlite3.Connection, product_id: int):
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products WHERE id=?", (product_id,))
    return cur.fetchone()


def create_order(conn: sqlite3.Connection, product_id: int, amount: int) -> str:
    order_id = "ORD_" + uuid.uuid4().hex[:18].upper()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders(id, product_id, amount, status, created_at) VALUES(?,?,?,?,?)",
        (order_id, product_id, amount, "결제대기", int(time.time())),
    )
    conn.commit()
    return order_id


def get_order(conn: sqlite3.Connection, order_id: str):
    cur = conn.cursor()
    cur.execute("SELECT id, amount, status FROM orders WHERE id=?", (order_id,))
    return cur.fetchone()


def update_order_status(conn: sqlite3.Connection, order_id: str, status: str):
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    conn.commit()


def list_products(conn: sqlite3.Connection):
    cur = conn.cursor()
    cur.execute("SELECT id, name, price FROM products ORDER BY id ASC")
    return cur.fetchall()


def create_product(conn: sqlite3.Connection, name: str, price: int) -> int:
    cur = conn.cursor()
    cur.execute("INSERT INTO products(name, price) VALUES(?,?)", (name, price))
    conn.commit()
    return cur.lastrowid
