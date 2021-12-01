from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
import datetime

from .models.product import Product
from .models.product import ProductSummary
from .models.product_sellers import SellerSummary
from .models.inventory import Inventory
from .models.purchase import Purchase
from .models.seller_review import SellerReview
from .models.product_review import ProductReview
from .models.product_review import ProductReviewWithName
from .models.cart import cart


from flask import Blueprint
bp = Blueprint('cart', __name__)

# cart_page html
@bp.route('/cart_page')
def cart_page():
    # find the products current user has bought:
    if current_user.is_authenticated:
        carts = cart.get_all_cart_input(user_id = current_user.id)
        price = cart.get_total_price(user_id = current_user.id)
    else:
        carts = None

    return render_template('cart_page.html',
                           cart_content = carts,
                           total_price = price)

# cart_update html
@bp.route('/cart_update/<uid>/<sid>/<pid>/<quan>/<price>', methods = ['POST', 'GET'])
def cart_update(uid, sid, pid, quan, price):

    return render_template('cart_update.html',
                           user_id = uid,
                           seller_id = sid,
                           product_id = pid,
                           quantity = quan,
                           price_per_item = price)


# delete_cart_element
@bp.route('/delete_cart_element/<user_id>/<seller_id>/<product_id>/', methods = ['POST', 'GET'])
def delete_cart_element(user_id, seller_id, product_id):
    cart.remove_product_in_cart(user_id = user_id, seller_id = seller_id, product_id = product_id)

    return redirect(url_for('index.cart_page'))

#update_cart_quantity
@bp.route('/update_cart_quantity/<user_id>/<seller_id>/<product_id>/<quantity>/', methods = ['POST', 'GET'])
def update_cart_quantity(user_id, seller_id, product_id, quantity):
    cart.update_cart(user_id = user_id, seller_id = seller_id, product_id = product_id, quantity = quantity)

    return redirect(url_for('index.cart_page'))

#update_cart_quantity
@bp.route('/purchase_from_cart/<user_id>/', methods = ['POST', 'GET'])
def purchase_from_cart(user_id):
    if cart.check_order(user_id = user_id): 
        cart.make_cart_order(user_id = user_id)

    return redirect(url_for('index.cart_page'))