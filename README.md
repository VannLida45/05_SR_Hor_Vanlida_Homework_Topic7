
# Safe Shopping Agent

## 1. Project Overview

A simple AI shopping assistant built with Python,
Ollama and Pydantic.

The agent can search for products, check stock and
delete products according to user permissions.

## 2. Available Tools


| search_products : Search by product name |
| check_stock : Check stock by product ID |
| delete_product : Delete one product |

## 3. Agent Loop

User Request
    ↓
LLM decides whether to use a tool
    ↓
LLM requests a tool with arguments
    ↓
Harness checks permission and validates inputs
    ↓
Application executes the tool
    ↓
Tool result returns to the LLM
    ↓
LLM decides whether to continue or finish

## 4. Permission Rules

Customer can:
    - search_products 
    - check_stock 
    - buy_product

Admin can: 
    - search_products 
    - check_stock 
    - buy_product
    - delete_product

Permissions are enforced in harness.py.

## 5. Safety

- Pydantic validates tool inputs.
- The harness checks permissions.
- Unknown tools are rejected.
- Errors return controlled results.
- The agent has a maximum of five iterations.

## 6. Installation

Requirements:
- Python 3.10 or newer
- Ollama

Install Python packages:

    python -m pip install -r requirements.txt

Download the local model:

    ollama pull llama3.2:3b

Ensure Ollama is running.

## 7. Run the Application

    python main.py

Choose customer or admin, then enter a request.

## 8. Example Run

Add actual terminal output from the following tests:

1. Customer searches for an available laptop.
-------------------------------------------------

==================================================
            SAFE SHOPPING AGENT
==================================================
Enter your role (customer/admin): customer

You can start chatting with the shopping agent.
Type 'goodbye' to exit.

You: check all product that are in stock

==================================================
AGENT STARTED
==================================================
Role: customer
Request: check all product that are in stock

--- Iteration 1 ---

TOOL REQUEST
Tool: search_products
Arguments: {'query': 'all'}

TOOL RESULT
{'success': True, 'products': [{'id': 2, 'name': 'Dell Laptop', 'price': 850.0, 'stock': 5}, {'id': 3, 'name': 'iPhone 15', 'price': 750.0, 'stock': 7}, {'id': 4, 'name': 'HP Laptop', 'price': 700.0, 'stock': 12}]}

--- Iteration 2 ---

FINAL ANSWER:
Here are the products that are in stock:

1. Dell Laptop - Available with 5 units in stock
2. iPhone 15 - Available with 7 units in stock
3. HP Laptop - Available with 12 units in stock

If you'd like to check a specific product's availability, please let me know its name or ID!

---------------------------------------------------------------


2. Customer attempts to delete a product.

-------------------------------------------------

==================================================
            Ready for your next request.
==================================================
You: delete all products

==================================================
AGENT STARTED
==================================================
Role: customer
Request: delete all products

--- Iteration 1 ---

TOOL REQUEST
Tool: delete_product
Arguments: {'product_id': 'null'}

TOOL RESULT
{'success': False, 'error': 'PERMISSION_DENIED', 'message': 'customer cannot use delete_product.'}

--- Iteration 2 ---

FINAL ANSWER:
I apologize for the error. It seems that the customer does not have permission to delete all products.

If you are an authorized administrator, please let me know and I can assist with deleting all products. Alternatively, if you'd like to remove a specific product from stock, I can help with that as well!

---------------------------------------------------------------

3. Admin deletes a product.

---------------------------------------------------------------

You: delete product with id 3

==================================================
AGENT STARTED
==================================================
Role: admin
Request: delete product with id 3

--- Iteration 1 ---

TOOL REQUEST
Tool: delete_product
Arguments: {'product_id': 3}

TOOL RESULT
{'success': True, 'message': 'iPhone 15 deleted successfully.', 'product_id': 3}

--- Iteration 2 ---

FINAL ANSWER:
The product with ID 3 has been successfully deleted from the database.

---------------------------------------------------------------

## 9. Project Structure

- main.py: Application entry point
- agent.py: LLM and agent loop
- tools.py: Product operations
- schemas.py: Pydantic validation
- harness.py: Permissions and safety
- config.py: Model configuration and sample data