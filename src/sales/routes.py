from flask import request, Blueprint, current_app

sales_bp = Blueprint("sales", __name__, url_prefix="/sales")

@sales_bp.post("")
def make_sale():
    """
    POST /sales processes sale of line-items included in request.
    """
    return current_app.sales_service.process_sale(request.get_json())