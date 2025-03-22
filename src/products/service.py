from db import db, Product

def list_products() -> list[dict]:
    """
    Retrieve all products from the database.

    Queries the Product model to fetch all product records and returns a list of dictionaries,
    where each dictionary contains the product's 'id', 'name', and 'price'.

    Returns:
        list[dict]: A list of dictionaries representing products.
                    Example:
                    [
                        {"id": 1, "name": "Chrome Toaster", "price": 100},
                        {"id": 2, "name": "Copper Kettle", "price": 49.99},
                        {"id": 3, "name": "Mixing Bowl", "price": 20}
                    ]
    """
    return [{"id": p.id, "name": p.name, "price": p.price} for p in Product.query.all()]

def create_product(data: dict) -> dict:
    """
    Create a new product using the provided data.

    This function validates the input data to ensure that it contains the required 'name' and 'price' keys 
    with proper types. On successful validation, it creates a new Product instance, adds it to the database, 
    and commits the transaction. It returns a dictionary representation of the newly created product.
    
    If the input data fails validation, a ValueError is raised and caught, and the function returns a tuple 
    containing an error dictionary and a 400 status code.

    Args:
        data (dict): A dictionary containing the product details. Must include:
                     - 'name' (str): The name of the product.
                     - 'price' (float or int): The price of the product.

    Returns:
        dict: A dictionary with the new product's details on success.
              Example: {"id": 4, "name": "Microwave", "price": 200}
        tuple: In case of a validation error, returns a tuple with an error message and HTTP status code 400.
               Example: ({"error": "Request must include name and price."}, 400)
    """
    try:
        validate_post_request(data)
        new_product = Product(name = data["name"], price=data["price"])
        db.session.add(new_product)
        db.session.commit()
        return {"id": new_product.id, "name": new_product.name, "price": new_product.price}
    except (ValueError, TypeError) as e:
        return {"error":str(e)}, 400

def validate_post_request(data: dict):
    """
    Validate the input data for creating a product.

    Ensures that the provided dictionary is not empty and contains both the 'name' and 'price' keys.
    Additionally, it checks that the 'name' is a string and the 'price' is either an int or a float.
    
    Raises:
        ValueError: If the data is empty, missing required keys, or invalid.
                   - Missing keys: "Request must include name and price."
                   - Invalid value: "'price' must be > 0."
        TypeError: If the data values are not of the correct data types.
                   - Incorrect type for 'name': "'name' must be of type string."
                   - Incorrect type for 'price': "'price' must be of type float or int."
    Args:
        data (dict): The input dictionary to be validated.
    """
    if not data or not ({'name', 'price'} <= data.keys()):
        raise ValueError('Request must include name and price.')
    if type(data['name']) is not str:
        raise TypeError("'name' must be of type string.")
    if type(data['price']) not in [float, int]:
        raise TypeError("'price' must be of type float or int.")
    if data["price"] <= 0:
        raise ValueError("'price' must be > 0.")