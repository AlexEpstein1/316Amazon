from flask import current_app as app


class Inventory:
    # def __init__(self, id, name, price, cat_name, description, image_file, available):
    #     self.id = id
    #     self.name = name
    #     self.cat_name = cat_name
    #     self.price = price
    #     self.description = description
    #     self.image_file = image_file
    #     self.available = available

    def __init__(self, seller_id, product_id, price, prod_name, stock, firstname, lastname):
            self.seller_id = seller_id
            self.product_id = product_id
            self.price = price
            self.prod_name = prod_name
            self.stock = stock
            self.firstname = firstname
            self.lastname = lastname

        

    # def __repr__():
    #     return ""

    @staticmethod
    def get(seller_id):
        rows = app.db.execute('''
        SELECT seller_id, product_id, price, stock
            FROM SellsItem
            WHERE seller_id = :seller_id
        ''',
        seller_id=seller_id)
        return Inventory(*(rows[0])) if rows is not None else None


    @staticmethod
    def get_all(available=True, seller_id=None):
        if seller_id is None:
            rows = app.db.execute('''
            SELECT si.seller_id, si.product_id, si.price, p.name, si.stock, u.firstname, u.lastname
            FROM SellsItem si, Products p, Users u
            WHERE si.product_id = p.id AND u.id = si.seller_id
            ORDER BY si.seller_id
            
            '''.format(available),
            available=available)
            return [Inventory(*row) for row in rows]
        else:
            rows = app.db.execute('''
            SELECT s.seller_id, s.product_id, s.price, s.stock, p.name
            FROM SellsItem s, Products p
            WHERE s.seller_id = :seller_id AND s.product_id = p.id 
            ''',
            seller_id=seller_id)
            return [Inventory(*row) for row in rows]
    
    @staticmethod
    def productList(id):
        rows = app.db.execute('''
        SELECT s.product_id, s.price, s.stock, s.seller_id, u.firstname, u.lastname
        FROM SellsItem s, Users u
        WHERE s.product_id = :id AND s.seller_id = u.id
        ''',
        id=id)
        return [Inventory(*row) for row in rows] if rows is not None else 'No current sellers'


