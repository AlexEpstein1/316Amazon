from flask import redirect, render_template, request, url_for
from flask_login import current_user
import statistics
import datetime

from .models.product import Product
from .models.product import ProductSummary
from .models.product import ProductSellers
from .models.purchase import Purchase
from .models.seller_review import SellerReview
from .models.product_review import ProductReview
from .models.product_review import ProductReviewWithName

from flask import Blueprint
bp = Blueprint('reviews', __name__)

def get_prod_info(product_id):
    # Get previous user review for the product
    prev_review = ProductReview.get(user_id = current_user.id,
                                    product_id = product_id)
    # Get product information
    # products = Product.get_all(available = False,
    #                            id = product_id)
    # Get product summary
    product_summary = ProductSummary.get(product_id = product_id)

    info = {
    "prev_review": prev_review,
    # "products": products[0],
    "product_summary": product_summary[0]
    }

    return info

# Direct to front-end submit product review
@bp.route('/write_prod_review/<product_id>', methods = ['POST', 'GET'])
def write_prod_review(product_id):

    info = get_prod_info(product_id = product_id)

    return render_template('submit_prod_review.html',
                           product_id = product_id,
                           # products = info.get('products'),
                           prev_review = info.get('prev_review'),
                           product_summary = info.get('product_summary'),
                           review_submitted = False)

# Backend for submit product review
@bp.route('/add_prod_review/<product_id>/<update>', methods = ['POST', 'GET'])
def add_prod_review(product_id, update):
    print(update)
    # If adding new review (update = False)
    if update == 'False':
        print('here')
        result = ProductReview.add_prod_review(request = request,
                                               product_id = product_id)
    # If editing/updating review
    else:
        print('not here')
        result = ProductReview.update_review(request = request,
                                             product_id = product_id)

    info = get_prod_info(product_id = product_id)

    return render_template('submit_prod_review.html',
                           product_id = product_id,
                           # products = info.get('products'),
                           prev_review = info.get('prev_review'),
                           product_summary = info.get('product_summary'),
                           review_submitted = True,
                           result = result)

# Backend for deleting product review
@bp.route('/delete_prod_review/<product_id>/', methods = ['POST', 'GET'])
def delete_prod_review(product_id):

    result = ProductReview.delete_review(product_id = product_id)
    # print(result)
    return redirect(url_for('index.review_history'))
