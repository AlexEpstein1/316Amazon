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
from .models.inventory import Inventory


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

@bp.route('/seller_product/<id>', methods = ['POST', 'GET'])
def seller_product(id):
    product = Product.get(id)
    sellers = ProductSellers.productSellers(id=id)
    reviews = ProductReviewWithName.get_reviews(product_id=id)
    avg_rating = get_avg(reviews)
    seller_id = current_user.id
    return render_template('seller_product.html',
                           product=product,
                            sellers=sellers,
                            reviews=reviews,
                            avg_rating=avg_rating,
                            seller_id=seller_id
                            )

@bp.route('/add_product/<id>', methods = ['POST', 'GET'])
def add_product(id):
    # get all available products for sale:
    product = Product.get(id)
    seller_id = current_user.id
    mode = "add"
    # check if we already sell this item 

    if ProductSellers.alreadySells(id): 
        products = Product.get_all(available=True)
        return render_template('create_product.html',
                           products=products,
                           message="You already sell this item!")
    else: 
        return render_template('add_product_page.html',
                           product=product,
                           seller=seller_id,
                           mode=mode)

@bp.route('/edit_product/<id>', methods = ['POST', 'GET'])
def edit_product(id):
    # get all available products for sale:
    product = Product.get(id)
    seller_id = current_user.id
    mode="edit"
    seller_product = Inventory.getProduct(id)

    return render_template('add_product_page.html',
                           product=product,
                           seller_product=seller_product,
                           seller=seller_id,
                           editing=True,
                           mode=mode)




@bp.route('/write_product/<id>/<mode>', methods = ['POST', 'GET'])
def write_product(id, mode):
    # get all available products for sale:
    # product = Product.get(id)

    # If valid inputs, call product.write_product 
    if mode == "add":
        message = ProductSellers.addProduct(id=id, request=request)
    else: 
        message = ProductSellers.editProduct(id=id, request=request)
    
    # else prompt the user again 
    inventory = Inventory.get_all(available=True, seller_id=current_user.id)

    product=Product.get(id)

    if mode == "add":
        return render_template('inventory.html',
                           sold_products=inventory,
                           message=message + product.name + " to your inventory")
    else: 
        message = ProductSellers.editProduct(id=id, request=request)
        return render_template('inventory.html',
                           sold_products=inventory,
                           message=message + product.name)
                        #    Need to have this go to seller_product page once it's added to the DB 

@bp.route('/delete_product/<id>', methods = ['POST', 'GET'])
def delete_product(id):
    # get all available products for sale:
    # product = Product.get(id)

    # If valid inputs, call product.write_product 

    # added = ProductSellers.addProduct(id=id, request=request)
    product=Product.get(id)
    # else prompt the user again 
    message = ProductSellers.deleteProduct(id=id)

    inventory = Inventory.get_all(available=True, seller_id=current_user.id)



    return render_template('inventory.html',
                           sold_products=inventory,
                           message=message+product.name + " from your inventory")

