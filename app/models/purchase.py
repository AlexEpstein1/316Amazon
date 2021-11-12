from flask import current_app as app


class Purchase:
    def __init__(self, order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, status):
        self.order_id = order_id
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.payment_amount = payment_amount
        self.quantity = quantity
        self.time_purchased = time_purchased
        self.status = status

    @staticmethod
    def get(order_id):
        rows = app.db.execute('''
SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, status
FROM Purchases
WHERE order_id = :order_id
''',
                              order_id=order_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_buyer_id(buyer_id):
        rows = app.db.execute('''
SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, status
FROM Purchases
WHERE buyer_id = :buyer_id
ORDER BY time_purchased DESC
''',
                              buyer_id=buyer_id)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_buyer_id_since(buyer_id, since):
        rows = app.db.execute('''
SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, status
FROM Purchases
WHERE buyer_id = :buyer_id
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              buyer_id=buyer_id,
                              since=since)
        return [Purchase(*row) for row in rows]

    
