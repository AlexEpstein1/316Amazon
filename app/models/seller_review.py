from flask import current_app as app, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import exc
import datetime

# Reviews of Sellers
# CREATE TABLE SellerReview (
# 	user_id INT NOT NULL REFERENCES Users(id),
# 	seller_id INT NOT NULL REFERENCES Sellers(id),
# 	date_time DATE NOT NULL,
# 	description VARCHAR(256) NOT NULL,
# 	rating DECIMAL(10, 2) NOT NULL CHECK(rating >= 1 AND rating <= 5),
# 	PRIMARY KEY (user_id, seller_id)
# 	FOREIGN KEY (user_id, seller_id) REFERENCES Purchases(uid, pid)
# );

class SellerReview:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.seller_id = kwargs.get('seller_id')
        self.date_time = kwargs.get('date_time')
        self.description = kwargs.get('description', '')
        self.rating = kwargs.get('rating')
        self.exists = kwargs.get('exists')
        self.reviews = kwargs.get('reviews')
        self.last_review = kwargs.get('last_review')
        self.avg_rating = kwargs.get('avg_rating')

    @staticmethod
    def get(user_id, seller_id = None):
        # If no passed in `seller_id`, then just return all reviews from that user
        if seller_id is None:
            rows = app.db.execute('''
            SELECT user_id, seller_id, date_time, description, rating
            FROM SellerReview
            WHERE user_id = :user_id
            ORDER BY date_time DESC
            ''',
                                  user_id = user_id)
        # If `seller_id` passed in, then return review from that user for the given seller_id
        else:
            rows = app.db.execute('''
            SELECT user_id, seller_id, date_time, description, rating
            FROM SellerReview
            WHERE user_id = :user_id AND seller_id = :seller_id
            ''',
                                  user_id = user_id,
                                  product_id = seller_id)

        # If there exists a previous review, create the object
        if rows:
            reviews = [SellerReview(user_id = row[0],
                                     seller_id = row[1],
                                     date_time = row[2],
                                     description = row[3],
                                     rating = row[4],
                                     exists = True) for row in rows]
            if seller_id is None:
                return reviews
            else:
                return reviews[0]

        # Otherwise, create an empty SellerReview object
        else:
            return(SellerReview(exists = False))

    # @staticmethod
    # def add_prod_review(request, product_id):
    #     # Get information to add to review
    #     date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    #     description = request.form['body']
    #     rating = request.form['numstars']
    #
    #     try:
    #         rows = app.db.execute("""
    #     INSERT INTO ProductReview(user_id, product_id, date_time, description, rating)
    #     VALUES(:user_id, :product_id, :date_time, :description, :rating)
    #     RETURNING user_id
    #     """,
    #                   user_id = current_user.id,
    #                   product_id = product_id,
    #                   date_time = date_time,
    #                   description = description,
    #                   rating = rating)
    #     # this means already a review for this product from this user
    #     except exc.IntegrityError as e:
    #         return False
    #
    #     return True
    #
    # @staticmethod
    # def update_review(request, product_id):
    #
    #     date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    #     description = request.form['body']
    #     rating = request.form['numstars']
    #
    #     rows = app.db.execute("""
    # UPDATE ProductReview
    # SET rating = :rating, description = :description
    # WHERE user_id = :user_id AND product_id = :product_id
    # RETURNING user_id
    # """,
    #               rating = rating,
    #               description = description,
    #               user_id = current_user.id,
    #               product_id = product_id)
    #
    #     return True
    #
    # @staticmethod
    # def delete_review(product_id):
    #     rows = app.db.execute("""
    # DELETE FROM ProductReview
    # WHERE user_id = :user_id AND product_id = :product_id
    # RETURNING user_id
    # """,
    #               user_id = current_user.id,
    #               product_id = product_id)
    #     # flash('Deleted product review for product ID: ' + product_id)
    #     return 'Deleted product review for product ID: ' + product_id
    @staticmethod
    def get_seller_review_stats(user_id):

        rows = app.db.execute('''
        SELECT user_id, COUNT(*) AS reviews, MAX(date_time) AS last_review, AVG(rating) AS avg_rating
        FROM SellerReview
        WHERE user_id = :user_id
        GROUP BY user_id
        ''',
                              user_id = user_id)

        # If there exists a previous review, create the object
        if rows:
            return [SellerReview(user_id = row[0],
                                 reviews = row[1],
                                 last_review = row[2],
                                 avg_rating = row[3],
                                 exists = True) for row in rows][0]

        # Otherwise, create an empty SellerReview object
        else:
            return (SellerReview(exists = False))
