from db import db, Product

def list_products() -> list[dict]:
    """
    Return a list of products with their ID, name, and price.
    """
    return [{"id": p.id, "name": p.name, "price": p.price} for p in Product.query.all()]

def create_product(data: dict) -> dict:
    """
    Create a new product given data that includes 'name' and 'price'.
    """
    try:
        validate_post_request(data)
        new_product = Product(name = data["name"], price=data["price"])
        db.session.add(new_product)
        db.session.commit()
        return {"id": new_product.id, "name": new_product.name, "price": new_product.price}
    except ValueError as e:
        return ({"error":str(e)}), 400

def validate_post_request(data: dict):
    """
    Validate that the request payload data is not empty, 
    and contains both 'name' and 'price' keys."
    """
    if not data or not ({'name', 'price'} <= data.keys()):
        raise ValueError('Request must include name and price.')
    if type(data['name']) is not str:
        raise ValueError("'name' must be of type string.")
    if type(data['price']) not in [float, int]:
        raise ValueError("'price' must be of type float or int.")