
from decimal import Decimal

from psycopg2.extras import RealDictCursor

from db import get_connection


def search_products(query: str):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:

            if query.strip().lower() in ("all", "all products", "*"):
                cursor.execute("""
                    SELECT id, name, price, stock
                    FROM products
                    ORDER BY id
                """)

            else:
                cursor.execute("""
                    SELECT id, name, price, stock
                    FROM products
                    WHERE name ILIKE %s
                    ORDER BY id
                """, (f"%{query}%",))

            products = cursor.fetchall()

            return {
                "success": True,
                "products": [
                    {
                        "id": p["id"],
                        "name": p["name"],
                        "price": float(p["price"]),
                        "stock": p["stock"]
                    }
                    for p in products
                ]
            }

    finally:
        conn.close()


def buy_product(product_id: int):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:

            cursor.execute(
                """
                UPDATE products
                SET stock = stock - 1
                WHERE id = %s
                  AND stock > 0
                RETURNING id, name, price, stock
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:
                conn.rollback()

                return {
                    "success": False,
                    "error": "OUT_OF_STOCK",
                    "message": "Product does not exist or is out of stock."
                }

            conn.commit()

            return {
                "success": True,
                "message": "Product purchased successfully.",
                "product_id": product["id"],
                "name": product["name"],
                "price": float(product["price"]),
                "remaining_stock": product["stock"]
            }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

def check_stock(product_id: int):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, name, stock
                FROM products
                WHERE id = %s
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:
                return {
                    "success": False,
                    "error": "PRODUCT_NOT_FOUND",
                    "message": "Product does not exist.",
                }

            return {
                "success": True,
                "product_id": product["id"],
                "name": product["name"],
                "stock": product["stock"],
                "available": product["stock"] > 0,
            }

    finally:
        conn.close()


def delete_product(product_id: int):
    conn = get_connection()

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                DELETE FROM products
                WHERE id = %s
                RETURNING id, name
                """,
                (product_id,)
            )

            product = cursor.fetchone()

            if product is None:
                conn.rollback()

                return {
                    "success": False,
                    "error": "PRODUCT_NOT_FOUND",
                    "message": "Product does not exist.",
                }

            conn.commit()

            return {
                "success": True,
                "message": f"{product['name']} deleted successfully.",
                "product_id": product["id"],
            }

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()