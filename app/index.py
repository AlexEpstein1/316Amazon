from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
import datetime

from .models.product import Product
from .models.inventory import Inventory
from .models.purchase import Purchase
from .models.seller_review import SellerReview
from .models.product_review import ProductReview
from .models.product_review import ProductReviewWithName

from flask import Blueprint
bp = Blueprint('index', __name__)

# index html
def get_avg(id):
    reviews = ProductReviewWithName.get_reviews(product_id=id)
    avg_rating = 0
    if reviews:
        for x in reviews:
            avg_rating+=x.rating
        avg_rating = avg_rating / len(reviews)
    return avg_rating


@bp.route('/')
def index():
    # get all available products for sale:
    products = Product.get_all(available=True)
    for x in products:
        x.rating = get_avg(x.id)
    categories = []
    for x in products:
        categories.append(x.cat_name)
    categories = set(categories)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_buyer_id_since(buyer_id = current_user.id,
                                                       since = datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None

    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           categories=categories)
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

# purchase_history html
@bp.route('/purchase_history')
def purchase_history():
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_buyer_id(buyer_id = current_user.id)
    else:
        purchases = None

    return render_template('purchase_history.html',
                           purchase_history=purchases)

# review_history html
@bp.route('/review_history')
def review_history():
    # if user is authenticated, go to home profile
    if current_user.is_authenticated:
        reviews = ProductReview.get(user_id = current_user.id)
        # print(reviews[0])
        return render_template('review_history.html',
                               reviews=reviews)
    # otherwise, back to index
    else:
        return redirect(url_for('index.index'))

    return render_template('index.html',
                           # message=message,
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
                           sold_products=inventory)
