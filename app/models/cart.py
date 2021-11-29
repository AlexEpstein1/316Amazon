from flask import current_app as app


'''
--- Carts Guru
-- Cart
CREATE TABLE Cart (
	user_id INT NOT NULL REFERENCES Users(id),
	seller_id INT NOT NULL REFERENCES Users(id),
	product_id INT NOT NULL REFERENCES Products(id),
	quantity INT NOT NULL CHECK(quantity >= 0),
	price_per_item DECIMAL(10, 2) NOT NULL CHECK(price_per_item >= 0),
	PRIMARY KEY(user_id, seller_id, product_id)
);
'''

class cart:
    def __init__(self, user_id, seller_id, product_id, quantity, price_per_item):
        self.user_id = user_id
        self.seller_id = seller_id
        self.product_id = product_id
        self.quantity = quantity
        self.price_per_item = price_per_item
    
    @staticmethod
    # method to get the exact line in the cart 
    def get(user_id, seller_id, product_id):
        rows = app.db.execute('''
            SELECT user_id, seller_id, product_id, quantity, price_per_item
            FROM Cart
            WHERE user_id = :user_id, seller_id = seller_id, product_id = product_id
            ''',
                              user_id = user_id, seller_id = seller_id, product_id = product_id)
        return cart(*(rows[0])) if rows else None   

    @staticmethod
    # get all cart input of a user
    def get_all_cart_input(user_id):
        rows = app.db.execute('''
            SELECT user_id, seller_id, product_id, quantity, price_per_item
            FROM Cart
            WHERE user_id = :user_id
            ''',
                              user_id = user_id)
        return [cart(*row) for row in rows]

    
    @staticmethod
    # method to calculate the total price of products in the cart 
    def get_total_price(user_id):
        total = 0
        cart_content = cart.get_all_cart_input(user_id)
        
        for c in cart_content:
            total += c.price_per_item*c.quantity
        
        return total

    @staticmethod
    # backend method to add product to cart of a user
    def add_to_cart(user_id, seller_id, product_id, quantity):
        quant = int(quantity)
        price_per_item = app.db.execute('''
            SELECT price
            FROM SellsItem
            WHERE product_id = :product_id AND seller_id = :seller_id
            ''',
                              product_id = product_id, seller_id = seller_id)
        app.db.execute('''
            INSERT INTO Cart(user_id, seller_id, product_id, quantity, price_per_item)
            VALUES(:user_id, :seller_id, :product_id, :quantity, :price_per_item)
            RETURNING user_id
            ''',
                              user_id = user_id, seller_id = seller_id, product_id = product_id, quantity=quantity, price_per_item=price_per_item)

    @staticmethod
    # backend method to update quantity of product in cart
    def update_cart(user_id, seller_id, product_id, quantity):
        quantity = int(quantity)
        app.db.execute('''
        UPDATE Cart
        SET quantity = :quantity
        WHERE user_id = :user_id AND seller_id = :seller_id AND product_id = :product_id
        RETURNING user_id
            ''',
                              user_id = user_id, seller_id = seller_id, product_id = product_id, quantity = quantity)

    @staticmethod
    # backend method to remove product in cart
    def remove_product_in_cart(user_id, seller_id, product_id):
        app.db.execute('''
        DELETE FROM Cart
        WHERE user_id = :user_id AND seller_id = :seller_id AND product_id = :product_id
        RETURNING user_id
            ''',
                              user_id = user_id, seller_id = seller_id, product_id = product_id)
        

