from db import db, Product

def list_products() -> list[dict]:
    """
    Return a list of products with their ID, name, and price.
    """
    return [{"id": p.id, "name": p.name, "price": p.price} for p in Product.query.all()]