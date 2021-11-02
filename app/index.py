from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.seller_review import SellerReview
from .models.product_review import ProductReview

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(available=True)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_buyer_id_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases)

@bp.route('/write_prod_review/<product_id>', methods = ['POST', 'GET'])
def write_prod_review(product_id):
    # print(product_id)

    products = Product.get_all(available=False, id=product_id)
    # print(products)

    return render_template('submit_prod_review.html',
                           product_id = product_id,
                           products = products[0])

@bp.route('/add_prod_review/<product_id>/', methods = ['POST', 'GET'])
def add_prod_review(product_id):
    print(product_id)

    product_review = ProductReview.get(user_id = current_user.id)
    print(product_review)

    return None
