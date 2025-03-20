from flask import request, Blueprint, jsonify
from .service import process_sale

sales_bp = Blueprint("sales", __name__, url_prefix="/sales")

@sales_bp.post("")
def make_sale():
    """
    POST /sales processes sale of line-items included in request.
    """
    try:
        return jsonify(process_sale(request.get_json())), 200
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400