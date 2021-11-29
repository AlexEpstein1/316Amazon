from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
from flask.helpers import url_for
from werkzeug.utils import redirect
from .models.product import Product
from .models.product import ProductSummary
from .models.product_sellers import SellerSummary
from .models.inventory import Inventory
from .models.purchase import Purchase

from .models.cart import cart

from flask import Blueprint
bp = Blueprint('cart_function', __name__)

@bp.route('/delete_cart_element/<user_id>/<seller_id>/<product_id>/', methods = ['POST', 'GET'])
def delete_cart_element(user_id, seller_id, product_id):
    cart.remove_product_in_cart(user_id = user_id, seller_id = seller_id, product_id = product_id)

    return redirect(url_for('index.cart_page'))




