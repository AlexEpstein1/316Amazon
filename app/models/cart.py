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
    # method to get the exact input in the cart 
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
    #method to calculate the total price of products in the cart 
    def get_total_price(user_id):
        total = 0
        cart_content = cart.get_all_cart_input(user_id)
        
        for c in cart_content:
            total += c.price_per_item*c.quantity
        
        return total
        

