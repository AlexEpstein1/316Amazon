from flask import redirect, render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.inventory import Inventory
from .models.purchase import Purchase
from .models.seller_review import SellerReview
from .models.product_review import ProductReview

from flask import Blueprint
bp = Blueprint('index', __name__)

# index html
@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(available=True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_buyer_id_since(buyer_id = current_user.id,
                                                       since = datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)
# home_profile html
@bp.route('/profile')
def profile():
    # if user is authenticated, go to home profile
    if current_user.is_authenticated:
        return render_template('profile.html')
    # otherwise, back to index
    else:
        return redirect(url_for('index.index'))

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)


@bp.route('/inventory')
def inventory():
    # if user is authenticated, go to home profile
    inventory = Inventory.get_all(available=True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_buyer_id_since(buyer_id = current_user.id,
                                                       since = datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None

    return render_template('inventory.html',
                           avail_products=inventory,
                           purchase_history=purchases)

# review_history html
@bp.route('/review_history')
def review_history():
    # if user is authenticated, go to home profile
    if current_user.is_authenticated:
        reviews = ProductReview.get(user_id = current_user.id)
        print(reviews[0])
        return render_template('review_history.html',
                               reviews=reviews)
    # otherwise, back to index
    else:
        return redirect(url_for('index.index'))

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)
# direct to front-end submit product review
@bp.route('/write_prod_review/<product_id>', methods = ['POST', 'GET'])
def write_prod_review(product_id):
    # print(product_id)

    products = Product.get_all(available=False, id=product_id)
    # print(products)

    return render_template('submit_prod_review.html',
                           product_id = product_id,
                           products = products[0],
                           review_submitted = False)
# backend for submit product review
@bp.route('/add_prod_review/<product_id>/', methods = ['POST', 'GET'])
def add_prod_review(product_id):
    # print(product_id)
    # print(request.form)
    # product_review = ProductReview.get(user_id = current_user.id)
    # print(product_review)
    result = ProductReview.add_prod_review(request = request,
                                           product_id = product_id)

    products = Product.get_all(available=False, id=product_id)

    return render_template('submit_prod_review.html',
                           product_id = product_id,
                           products = products[0],
                           review_submitted = True,
                           result = result)
