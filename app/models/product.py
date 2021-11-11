from flask import current_app as app


class Product:
    def __init__(self, id, name, price, cat_name, description, image_file, available):
        self.id = id
        self.name = name
        self.cat_name = cat_name
        self.price = price
        self.description = description
        self.image_file = image_file
        self.available = available

    # def __repr__():
    #     return ""

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, name, price, cat_name, description, image_file, available
        FROM Products
        WHERE id = :id
        ''',
        id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True, id=None):
        if id is None:
            rows = app.db.execute('''
            SELECT id, name, price, cat_name, description, image_file, available
            FROM Products
            WHERE available = {0}
            '''.format(available),
            available=available)
            return [Product(*row) for row in rows]
        else:
            rows = app.db.execute('''
            SELECT DISTINCT id, name, price, cat_name, description, image_file, available
            FROM Products
            WHERE id = :id
            ''',
            id=id)
            return [Product(*row) for row in rows]

    @staticmethod
    def get_by_cat(cat):
        rows = app.db.execute('''
        SELECT id, name, price, cat_name, description, image_file, available
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
        return [ProductSellers(*row) for row in rows] if rows is not None else 'hi'

