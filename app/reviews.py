from flask import redirect, render_template, request, url_for
from flask_login import current_user
import statistics
import datetime

from .models.product import Product
from .models.product import ProductSellers
from .models.purchase import Purchase
from .models.seller_review import SellerReview
from .models.product_review import ProductReview
from .models.product_review import ProductReviewWithName

from flask import Blueprint
bp = Blueprint('reviews', __name__)

# Direct to front-end submit product review
@bp.route('/write_prod_review/<product_id>', methods = ['POST', 'GET'])
def write_prod_review(product_id):

    # Get review for this product if it exists
    prev_review = ProductReview.get(user_id = current_user.id,
                                    product_id = product_id)

    print(prev_review)
    # print(product_id)
    products = Product.get_all(available = False, id = product_id)
    # print(products)
    return render_template('submit_prod_review.html',
                           product_id = product_id,
                           products = products[0],
                           prev_review = prev_review[0],
                           # update = update,
                           review_submitted = False)

# backend for submit product review
@bp.route('/add_prod_review/<product_id>/<update>', methods = ['POST', 'GET'])
def add_prod_review(product_id, update):

    # If adding new review (update = False)
    if update == False:
        result = ProductReview.add_prod_review(request = request,
                                               product_id = product_id)
    # If editing/updating review
    else:
        result = ProductReview.update_review(request = request,
                                             product_id = product_id)

    products = Product.get_all(available = False,
                               id = product_id)
    # Get review for this product if it exists
    prev_review = ProductReview.get(user_id = current_user.id,
                                    product_id = product_id)

    return render_template('submit_prod_review.html',
                           product_id = product_id,
                           products = products[0],
                           prev_review = prev_review[0],
                           review_submitted = True,
                           result = result)

# backend for deleting product review
@bp.route('/delete_prod_review/<product_id>/', methods = ['POST', 'GET'])
def delete_prod_review(product_id):

    result = ProductReview.delete_review(product_id = product_id)
    print(result)
    return redirect(url_for('index.review_history'))
