from datetime import datetime, timedelta
from flask import current_app as app


class Purchase:
    def __init__(self, order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, time_processed, status):
        self.order_id = order_id
        self.product_id = product_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.payment_amount = payment_amount
        self.quantity = quantity
        self.time_purchased = time_purchased
        self.time_processed = time_processed
        self.status = status

    @staticmethod
    def get(order_id):
        rows = app.db.execute('''
SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, time_processed, status
FROM Purchases
WHERE order_id = :order_id
''',
                              order_id=order_id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_buyer_id(buyer_id, order_id = None):

        if order_id is None:
            rows = app.db.execute('''
            SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, time_processed,status
            FROM Purchases
            WHERE buyer_id = :buyer_id
            ORDER BY time_purchased DESC
            ''',
                                          buyer_id=buyer_id)
        else:
            rows = app.db.execute('''
            SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, time_processed, status
            FROM Purchases
            WHERE buyer_id = :buyer_id AND order_id = :order_id
            ORDER BY time_purchased DESC
            ''',
                                          buyer_id=buyer_id,
                                          order_id=order_id)

        return [Purchase(*row) for row in rows] if rows else None

    @staticmethod
    def get_all_by_buyer_id_since(buyer_id, since):
        rows = app.db.execute('''
SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, time_processed, status
FROM Purchases
WHERE buyer_id = :buyer_id
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              buyer_id=buyer_id,
                              since=since)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def update_order_status(buyer_id):
        status = 'Complete'
        time = datetime.now(tz=None) - timedelta(weeks= 2 )

        app.db.execute('''
            Update Purchases
            SET status = :status
            WHERE buyer_id = :buyer_id AND time_purchased <= :time
            RETURNING buyer_id
            ''',
                              buyer_id=buyer_id,
                              status = status,
                              time=time)

    
    @staticmethod
    def get_all_by_buyer_id_completed(buyer_id):
        status = 'Complete'

        rows = app.db.execute('''
SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, time_processed, status
FROM Purchases
WHERE buyer_id = :buyer_id
AND status = :status
ORDER BY time_purchased DESC
''',
                              buyer_id=buyer_id,
                              status=status)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_buyer_id_incomplete(buyer_id):
        status = 'Incomplete'

        rows = app.db.execute('''
SELECT order_id, product_id, buyer_id, seller_id, payment_amount, quantity, time_purchased, time_processed, status
FROM Purchases
WHERE buyer_id = :buyer_id
AND status = :status
ORDER BY time_purchased DESC
''',
                              buyer_id=buyer_id,
                              status=status)
        return [Purchase(*row) for row in rows]

