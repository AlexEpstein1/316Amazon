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
@bp.route('/review_history/<type>/<page>', methods = ['POST', 'GET'])
def review_history(type, page = 0):
    # Get offset to query as * 10 of page number
    # page 0 (0-9) 0, page 1 (10-19) 10, page 2 (20-29) 20
    page = int(page)
    offset = page * 10
    if type == 'products':
        product_id = ''
        reviews = ProductReview.get(user_id = current_user.id,
                                    offset = offset)
    elif type == 'sellers':
        product_id = ''
        reviews = SellerReview.get(user_id = current_user.id,
                                   offset = offset)
    elif type == 'product_history':
        product_id = request.args.get('product_id')
        reviews = ProductReview.get(user_id = None,
                                    product_id = product_id,
                                    offset = offset)
    # If `reviews` is returned as a list (means there is data)
    if isinstance(reviews, list):
        exists = True
    # Otherwise, just an empty object with .exists flag as False
    else:
        exists = reviews.exists

    return render_template('review_history.html',
                           page = page,
                           exists = exists,
                           product_id = product_id,
                           reviews = reviews,
                           type = type)

# reviews_landing html
@bp.route('/reviews_landing/<order_id>', methods = ['POST', 'GET'])
def reviews_landing(order_id):
    # If just a landing page to view either product or seller reviews
    if order_id == 'nav':
        # Get user information on their review history
        prod_stats = ProductReview.get_review_stats(user_id = current_user.id)
        seller_stats = SellerReview.get_review_stats(user_id = current_user.id)

        return render_template('reviews_landing.html',
                               prod_stats = prod_stats,
                               seller_stats = seller_stats)
    # Else, get the specific purchase to review
    purchase = Purchase.get_all_by_buyer_id(buyer_id = current_user.id,
                                            order_id = order_id)
    # This should never happen
    if purchase is None:
        return redirect(url_for('index.index'))

    # Get product and seller summary statistics
    product_summary = ProductSummary.get(product_id = purchase[0].product_id)
    seller_summary = SellerSummary.get(seller_id = purchase[0].seller_id)

    return render_template('reviews_landing.html',
                           purchase = purchase[0],
                           product_summary = product_summary[0],
                           seller_summary = seller_summary[0])

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
