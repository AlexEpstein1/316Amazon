from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user
import datetime

from .reviews import format_value

from .models.product import Product
from .models.product import ProductSummary
from .models.product_sellers import SellerSummary
from .models.inventory import Inventory
from .models.purchase import Purchase
from .models.seller_review import SellerReview
from .models.product_review import ProductReview
from .models.product_review import ProductReviewWithName
from .models.cart import cart
from .models.categories import Category


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
    categories = Category.get_all()

    return render_template('index.html',
                            categories=categories)

@bp.route('/createProduct', methods = ['POST', 'GET'])
def createProduct():
    # get all available products for sale:
    products = Product.get_first_ten(available=True, id = None)
    
    return render_template('create_product.html',
                           products=products,page=0)

@bp.route('/search_product', methods = ['POST', 'GET'])
def searchProducts(page=0):
    # get all available products for sale:
    if request is not None:
        body = request.form['body']
    else: 
        body=""
    first_search = True
    if body is None:
        products = Product.get_all(available=True)
    else: 
        products = Product.search(search=body, available=True)
        first_search = False
    return render_template('create_product.html',
                           products=products, 
                           search=body,
                           display_search=not first_search,
                           page=page)
# home_profile html
@bp.route('/profile')
def profile():
    # if user is authenticated, go to home profile
    if current_user.is_authenticated:
        return render_template('profile.html')
    # otherwise, back to index
    else:
        return redirect(url_for('index.index'))


# purchase_history html
@bp.route('/purchase_history')
def purchase_history():
    Purchase.update_order_status(buyer_id = current_user.id)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_buyer_id(buyer_id = current_user.id)
        complete_purchases = Purchase.get_all_by_buyer_id_completed(buyer_id = current_user.id)
        incomplete_purchases = Purchase.get_all_by_buyer_id_incomplete(buyer_id = current_user.id)
    else:
        purchases = None

    return render_template('purchase_history.html',
                           purchase_history=purchases,
                           complete_purchases= complete_purchases,
                           incomplete_purchases = incomplete_purchases)

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

        prod_stats.avg_rating = format_value(prod_stats.avg_rating, type = 'avg_rating')
        seller_stats.avg_rating = format_value(seller_stats.avg_rating, type = 'avg_rating')

        return render_template('reviews_landing.html',
                                order_id= order_id,
                               prod_stats = prod_stats,
                               seller_stats = seller_stats)

    # Else, get the specific purchase to review
    purchase = Purchase.get_all_by_buyer_id(buyer_id = current_user.id,
                                            order_id = order_id)
    # This should never happen
    if purchase is None:
        return redirect(url_for('index.index'))

    # Get product and seller summary statistics
    product_summary = ProductSummary.get(product_id = purchase[0].product_id)[0]
    seller_summary = SellerSummary.get(seller_id = purchase[0].seller_id)[0]

    product_summary.avg_price = format_value(product_summary.avg_price, type = 'avg_price')
    product_summary.avg_rating = format_value(product_summary.avg_rating, type = 'avg_rating')
    seller_summary.avg_price = format_value(seller_summary.avg_price, type = 'avg_price')
    seller_summary.avg_rating = format_value(seller_summary.avg_rating, type = 'avg_rating')

    return render_template('reviews_landing.html',
                           purchase = purchase[0],
                           product_summary = product_summary,
                           seller_summary = seller_summary)

@bp.route('/inventory/<page>')
def inventory(page = 0):

    # if user is authenticated, go to home profile
    inventory = Inventory.get_all(available=True, seller_id=current_user.id, offset=int(page)*10)
    
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_buyer_id_since(buyer_id = current_user.id,
                                                       since = datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None

    count = Inventory.countItems(current_user.id)
    

    return render_template('inventory.html',
                           sold_products=inventory,
                           page = int(page), 
                           count = count)

# cart_page html
@bp.route('/cart_page')
def cart_page():
    if current_user.is_authenticated:
        # find the products current user has in carts:
        carts = cart.get_all_cart_input(user_id = current_user.id)
        # find the products current user has saved:
        saved = cart.get_save_cart(user_id = current_user.id)
        # find total price of products in carts:
        price = cart.get_total_price(user_id = current_user.id)
    else:
        carts = None

    return render_template('cart_page.html',
                        saved_content = saved,  
                        cart_content = carts,
                        total_price = price)

@bp.route('/seller_history')
def seller_history():
    # find the products current user has bought:
    complete_purchases = Purchase.get_all_by_seller_id(seller_id = current_user.id, complete=True)
    incomplete_purchases = Purchase.get_all_by_seller_id(seller_id = current_user.id, complete=False)
    
    return render_template('seller_history.html',
                           complete_purchases=complete_purchases,
                           incomplete_purchases=incomplete_purchases)

