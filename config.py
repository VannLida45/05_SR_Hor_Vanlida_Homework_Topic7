
from shema import (
    SearchProductsInput,
    CheckStockInput,
    DeleteProductInput,
    BuyProductInput,
)

from tools import (
    search_products,
    check_stock,
    delete_product, buy_product,
)

MODEL_NAME = "llama3.2:3b"

MAX_ITERATIONS = 5

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Search products by name. "
                "If the user asks to show all products, "
                "use query='all'. "
                "Never use an empty query."
            ),
            "parameters": SearchProductsInput.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Check stock using a product ID.",
            "parameters": CheckStockInput.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "delete_product",
            "description": (
                "Delete one product by ID. "
                "Admin permission is required."
            ),
            "parameters": DeleteProductInput.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buy_product",
            "description": (
                "Buy one unit of a product. "
                "The product stock will decrease by 1. "
                "Only call this tool when the user clearly "
                "confirms that they want to buy the product."
            ),
            "parameters": BuyProductInput.model_json_schema(),
        },
    },
]


SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are a shopping assistant.\n\n"

        "Use tools to retrieve real product information.\n"

        "If the user asks to show or list all products, "
        "call search_products with query='all'.\n"

        "Never send an empty search query.\n"

        "Never invent product IDs, prices, or stock quantities.\n"

        "If the user asks about a product, search for that "
        "product before giving information.\n"

        "If the user says yes, yess, okay, or agrees to a "
        "previous question, use the previous conversation "
        "to understand what they agreed to.\n"

        "Do not claim an action succeeded unless the tool "
        "confirms success.\n"

        "If permission is denied, explain the denial.\n"

        "Never repeat a denied tool request."
    ),
}


TOOL_REGISTRY = {
    "search_products": (
        SearchProductsInput,
        search_products,
    ),
    "check_stock": (
        CheckStockInput,
        check_stock,
    ),
    "delete_product": (
        DeleteProductInput,
        delete_product,
    ),
"buy_product": (
        BuyProductInput,
        buy_product,
    ),
}


PERMISSIONS = {
    "customer": {
        "search_products",
        "check_stock",
        "buy_product",

    },
    "admin": {
        "search_products",
        "check_stock",
        "delete_product",
        "buy_product",
    },
}