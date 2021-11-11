from flask import redirect, render_template, request
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
bp = Blueprint('products', __name__)

def get_avg(reviews):
    avg_rating = 0
    if reviews:
        for x in reviews:
            avg_rating+=x.rating
        avg_rating = avg_rating / len(reviews)
    return avg_rating

def get_unique_cats(products):
    categories = []
    all_products = Product.get_all(available=True)
    for x in all_products:
        categories.append(x.cat_name)
    categories = set(categories)
    return categories


@bp.route('/filterCat/<cat>', methods = ['POST', 'GET'])
def filterCat(cat):
    products = Product.get_by_cat(cat=cat)
    categories = get_unique_cats(products)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = Purchase.get_all_by_buyer_id_since(buyer_id = current_user.id,
                                                       since = datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        purchases = None
    
    return render_template('index.html',
                           cat_name=cat,
                           avail_products=products,
                           purchase_history=purchases,
                           categories = categories)


@bp.route('/productPage/<id>', methods = ['POST', 'GET'])
def productPage(id):
    product = Product.get(id)
    sellers = ProductSellers.productSellers(id=id)
    reviews = ProductReviewWithName.get_reviews(product_id=id)
    avg_rating = get_avg(reviews)
    return render_template('productPage.html',
                           product=product,
                            sellers=sellers,
                            reviews=reviews,
                            avg_rating=avg_rating
                            )
