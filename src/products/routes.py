from flask import Blueprint, request, current_app
# from .service import list_products, create_product

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.get("")
def get_products():
    """
    GET /products returns a list of products.
    """
    return current_app.products_service.list_products()

@products_bp.post("")
def post_product():
    """
    POST /products adds the new product to the db,
    and returns the new product.
    """
    return current_app.products_service.create_product(request.get_json())