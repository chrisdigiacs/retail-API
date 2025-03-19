from flask import Blueprint, jsonify
from .service import list_products

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.get("")
def get_products():
    """
    GET /products returns a list of products.
    """
    return jsonify(list_products()), 200