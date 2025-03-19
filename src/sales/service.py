from db import Product, db

def process_sale(data: dict) -> dict:
    """
    Process a sale by validating the request, processing each line item,
    applying a discount, and calculating the total sale price.
    
    Args:
        data (dict): A dictionary containing the sale request. It must include:
            - "line_items": A list of line item dictionaries, each with "id" and "quantity".
            - "discount": An integer representing the flat discount for the sale.
    Returns:
        dict: A dictionary containing:
            - "line_items": A list of processed line items with calculated prices and discounts.
            - "total_sale_price": The sum of the prices for all line items after discount.
    Raises:
        ValueError or TypeError: If the sales request is invalid.
    """
    valid_sales_request(data)
    processed_line_items = [process_line_item(item) for item in data.get("line_items")]
    discount = data.get("discount", 0)
    processed_line_items = apply_discount(processed_line_items, discount)
    return {
        "line_items": processed_line_items,
        "total_sale_price": sum(item["price"] for item in processed_line_items)
    }

def apply_discount(line_items: list[dict], total_discount: int) -> list[dict]:
    """
    Distribute a flat discount evenly across all line items. The discount is
    spread proportionally by item count, with any rounding differences adjusted
    in the last item.
    
    Args:
        line_items (list): A list of dictionaries, each representing a line item.
            Each line item contains an id, quantity and price.
        total_discount (int or float): The total discount amount to be applied.
    Returns:
        list: The list of line items updated with a new key "discount" indicating
              the discount amount applied to each item.
    """
    accumulated_discount = 0
    num_items = len(line_items)
    for i in range(num_items):
        if i < num_items-1:
            item_discount = round((total_discount/num_items), 2)
            accumulated_discount += item_discount
        else:
            item_discount = round(total_discount - accumulated_discount, 2)
        line_items[i]["discount"] = item_discount
    return line_items

def process_line_item(item: dict) -> dict:
    """
    Process a single line item by validating the input, looking up the product,
    and calculating the total price for the given quantity.
    
    Args:
        item (dict): A dictionary with the keys "id" (product ID) and "quantity".
    Returns:
        dict: A dictionary representing the processed line item, including:
            - "id": The product ID.
            - "quantity": The quantity purchased.
            - "price": The total price calculated as quantity * product price.
    Raises:
        TypeError: If the product ID or quantity is not an integer.
        ValueError: If the quantity is not positive or the product is not found.
    """
    product_id = item.get("id")
    quantity = item.get("quantity")

    if type(product_id) is not int or type(quantity) is not int:
        raise TypeError("A product's ID and quantity must be integers.")
    if quantity <= 0:
        raise ValueError("Each product must have a positive purchase quantity.")
    
    product = product_lookup(product_id)
    item_total = item["quantity"]*product["price"]
    
    return {
        "id": product_id, 
        "quantity": quantity, 
        "price": item_total
        }

def product_lookup(product_id: int) -> dict:
    """
    Look up a product in the catalog by its ID.

    Args:
        product_id (int): The unique identifier of the product.
    Returns:
        dict: The product details containing "name" and "price".
    Raises:
        ValueError: If no product with the given ID is found.
    """
    product = db.session.get(Product, product_id)
    if not product:
        raise ValueError(f"Product with id {product_id} not found.")
    return {"name" : product.name, "price" : product.price}
    
def valid_sales_request(data: dict):
    """
    Validate the sales request data to ensure all required fields are present
    and of the correct type.

    Args:
        data (dict): The sales request data which must include:
            - "line_items": A list of line items.
            - "discount": An integer representing the discount amount.
    Raises:
        ValueError: If required fields are missing or if the list of line items is empty.
        TypeError: If "discount" is not an integer or "line_items" is not a list.
    """
    if data is None:
        raise ValueError("Request body is missing.")
    if "line_items" not in data:
        raise ValueError("Missing 'line_items' field.")
    if "discount" not in data:
        raise ValueError("Missing 'discount' field.")
    if type(data["discount"]) is not int:
        raise TypeError("'discount' must be an int.")
    if type(data["line_items"]) is not list:
        raise TypeError("'line_items' must be a list.")
    if len(data["line_items"]) < 1:
        raise ValueError("Request must include at least one line item.")