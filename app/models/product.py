from flask import current_app as app
from flask_login import current_user
from sqlalchemy import exc




class Product:
    def __init__(self, id, name, cat_name, description, image_file, available):
        self.id = id
        self.name = name
        self.cat_name = cat_name
        self.description = description
        self.image_file = image_file
        self.available = available

    # def __repr__():
    #     return ""

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, name, cat_name, description, image_file, available
        FROM Products
        WHERE id = :id
        ''',
        id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True, id=None):
        if id is None:
            rows = app.db.execute('''
            SELECT id, name, cat_name, description, image_file, available
            FROM Products
            WHERE available = {0}
            '''.format(available),
            available=available)
            return [Product(*row) for row in rows]
        else:
            rows = app.db.execute('''
            SELECT DISTINCT id, name, cat_name, description, image_file, available
            FROM Products
            WHERE id = :id
            ''',
            id=id)
            return [Product(*row) for row in rows]

            
    
    @staticmethod
    def search(search, available):
        # search products for product name 
            rows = app.db.execute('''
            SELECT id, name, price, cat_name, description, image_file, available
            FROM Products
            WHERE lower(name) LIKE lower(CONCAT(:search, '%'))
            '''.format(available),
            search=search,
            available=available)
            return [Product(*row) for row in rows]
       

    @staticmethod
    def get_by_cat(cat):
        rows = app.db.execute('''
        SELECT id, name, cat_name, description, image_file, available
        FROM Products
        WHERE cat_name = :cat
        ''',
        cat=cat)
        return [Product(*row) for row in rows]

class ProductSellers:
    def __init__(self, id, price, stock, seller_id, firstname, lastname):
        self.product_id = id
        self.price = price
        self.stock = stock
        self.seller_id = seller_id
        self.firstname = firstname
        self.lastname = lastname

    @staticmethod
    def productSellers(id):
        rows = app.db.execute('''
        SELECT s.product_id, s.price, s.stock, s.seller_id, u.firstname, u.lastname
        FROM SellsItem s, Users u
        WHERE s.product_id = :id AND s.seller_id = u.id
        ''',
        id=id)
        return [ProductSellers(*row) for row in rows] if rows is not None else 'No current sellers'

    @staticmethod
    def alreadySells(id):
        rows = app.db.execute('''
        SELECT s.product_id
        FROM SellsItem s
        WHERE s.product_id = :id AND s.seller_id = :seller_id
        ''',
        id=id, seller_id=current_user.id)
        return len(rows) > 0


    @staticmethod
    def addProduct(id, request): 
        stock = request.form["stock"]    
        price = request.form["price"]
        seller_id = current_user.id
    
        try:
            rows = app.db.execute("""
            INSERT INTO SellsItem(seller_id, product_id, price, stock)
            VALUES(:seller_id, :product_id, :price, :stock)
            RETURNING seller_id
            """,
                                  seller_id = seller_id,
                                  product_id = id,
                                  price = price,
                                  stock = stock)
        # this means already a review for this seller from this user
        except exc.IntegrityError as e:
            return False
        return 'Added product '

    @staticmethod
    def editProduct(id, request): 
        stock = request.form["stock"]    
        price = request.form["price"]
        seller_id = current_user.id
    
        rows = app.db.execute("""
        UPDATE SellsItem
        SET stock = :stock, price = :price
        WHERE seller_id = :seller_id AND product_id = :product_id
        RETURNING seller_id
        """,
                             seller_id=seller_id,
                             product_id=id,
                             price=price,
                             stock=stock)
        return "Edited Product "

    @staticmethod
    def deleteProduct(id): 
        seller_id=current_user.id
        rows = app.db.execute("""
        DELETE FROM SellsItem
        WHERE product_id = :product_id AND seller_id = :seller_id
        RETURNING seller_id
        """,
                              product_id = id,
                              seller_id = seller_id)
        # flash('Deleted product review for product ID: ' + product_id)
        return 'Deleted product '

    @staticmethod
    def add_new_product(user_id, request, num_products): 
        cat_name = request.form["cat_name"]    
        name = request.form["name"]
        description = request.form["description"]    
        price = request.form["price"]
        quantity = request.form["quantity"]
        seller_id = current_user.id
        available = True
        image_file='image'
        product_id = num_products+1
    
        
        app.db.execute("""
        INSERT INTO Products(product_id, name, cat_name, description, image_file, available)
        VALUES(:id, :name, :cat_name, :description, :image_file, :available)
        RETURNING 
        """,
                            id=product_id,
                            name=name,
                            cat_name=cat_name,
                            description=description,
                            image_file=image_file,
                            available=available
                            )
    
        return 'Added product '



class ProductSummary:
    def __init__(self, product_id, name, cat_name, description, sellers, avg_price, total_stock, reviews, avg_rating):
        self.product_id = product_id
        self.name = name
        self.cat_name = cat_name
        self.description = description
        self.sellers = sellers
        self.avg_price = avg_price
        self.total_stock = total_stock
        self.reviews = reviews
        self.avg_rating = avg_rating

    @staticmethod
    def get(product_id):
        rows = app.db.execute('''
        SELECT *
        FROM ProductSummary
        WHERE product_id = :product_id
        ''',
             product_id=product_id)

        return [ProductSummary(*row) for row in rows] if rows else None


